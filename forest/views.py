from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework_gis.filters import GeoFilterSet
from .models import Administration, chiefs, treeSpecies, treeNursery, TreeLoss
from .serializer import adminSerializer, chiefSerializer, speciesSerializer, treeNuserySerializer, treeLossSerializer
from rest_framework_gis.filters import InBBoxFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Sum
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
import ee
import geemap

def index(request):
    return render(request, 'dist/index.html')
# Create your views here.
class adminViewSet(viewsets.ModelViewSet):
    queryset = Administration.objects.all() #manager that returns queryset object same as SELECT * ALL FROM farms
    serializer_class = adminSerializer

class chiefViewSet(viewsets.ModelViewSet):
    queryset = chiefs.objects.all() #manager that returns queryset object same as SELECT * ALL FROM farms
    serializer_class = chiefSerializer

class nursuriesViewSet(viewsets.ModelViewSet):
    queryset = treeNursery.objects.all() #manager that returns queryset object same as SELECT * ALL FROM farms
    serializer_class = treeNuserySerializer
    filter_backends = (DjangoFilterBackend,)
    

    @action(detail=False, methods=["get"])
    def nurseries(self, request):
        longitude = request.GET.get("lng", None)
        latitude = request.GET.get("lat", None)

        if longitude and latitude:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            closest_nursery = treeNursery.objects.filter(
                geom__distance_lte=(user_location, D(km=5))
                #geom__contains=user_location
            )
            serializer = self.get_serializer_class()
            serialized_location = serializer(closest_nursery, many=True)
            return Response(serialized_location.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class treeSpeciesFilter(GeoFilterSet):
    location = filters.CharFilter(
        method="get_treeSpecies_by_location", lookup_expr="within"
    )

    class Meta:
        model = treeSpecies
        exclude = ["geom"]

    def get_treeSpecies_by_location(self, queryset, name, value):
        filtered_boundary = Administration.objects.filter(id=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            treeSpecies_in_location = queryset.filter(geom__within=boundary.geom)
        return treeSpecies_in_location
    
class speciesViewSet(viewsets.ModelViewSet):
    queryset = treeSpecies.objects.all() #manager that returns queryset object same as SELECT * ALL FROM farms
    serializer_class = speciesSerializer
    filterset_class = treeSpeciesFilter
    filter_backends = (DjangoFilterBackend,)

    @action(detail=False, methods=["get"])
    def species_within(self, request):
        longitude = request.GET.get("lng", None)
        latitude = request.GET.get("lat", None)

        if longitude and latitude:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            closest_nursery = treeSpecies.objects.filter(
                geom__contains=user_location
            )
            serializer = self.get_serializer_class()
            serialized_species = serializer(closest_nursery, many=True)
            return Response(serialized_species.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# latitude = 0.2
# longitude = 36

# pnt = Point(longitude,latitude, srid=4326)
# user_location = GEOSGeometry(pnt)

# class distView(viewsets.ModelViewSet):
#     model = Administration
#     # context_object_name = 'treeSpecies'
#     #queryset = treeSpecies.objects.filter(geom__contains=user_location)
#     queryset = Administration.objects.filter(geom__intersects=user_location)
#     serializer_class = adminSerializer
class treeNuseriesFilter(GeoFilterSet):
    location = filters.CharFilter(
        method="get_treeNursery_by_location", lookup_expr="within"
    )

    class Meta:
        model = treeNursery
        exclude = ["geom"]

    def get_treeNursery_by_location(self, queryset, name, value):
        filtered_boundary = Administration.objects.filter(id=value)
        if filtered_boundary:
            boundary = filtered_boundary.first()
            treeNursery_in_location = queryset.filter(geom__within=boundary.geom)
        return treeNursery_in_location
    
class distView(viewsets.ModelViewSet):
    #serializer_class = treeNuserySerializer
    serializer_class = adminSerializer
    queryset = treeNursery.objects.all()
    #bbox_filter_field = 'point'
    filterset_class = treeNuseriesFilter
    filter_backends = (DjangoFilterBackend,)
    #bbox_filter_include_overlapping = True

    @action(detail=False, methods=["get"])
    def get_Location(self, request):
        longitude = request.GET.get("lng", None)
        latitude = request.GET.get("lat", None)

        if longitude and latitude:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            closest_nursery = Administration.objects.filter(
                #geom__distance_lte=(user_location, D(km=10))
                geom__contains=user_location
            )
            serializer = self.get_serializer_class()
            serialized_location = serializer(closest_nursery, many=True)
            return Response(serialized_location.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=["get"])
    # def nurseries_locations(self, request):
    #     longitude = request.GET.get("lng", None)
    #     latitude = request.GET.get("lat", None)

    #     if longitude and latitude:
    #         user_location = Point(float(longitude), float(latitude), srid=4326)
    #         closest_nursery = Administration.objects.filter(
    #             geom__distance_lte=(user_location, D(km=5))
    #             #geom__contains=user_location
    #         )
    #         serializer = self.get_serializer_class()
    #         serialized_location = serializer(closest_nursery, many=True)
    #         return Response(serialized_location.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
class treeLossViewSet(viewsets.ModelViewSet):
    queryset = TreeLoss.objects.all() #manager that returns queryset object same as SELECT * ALL FROM farms
    serializer_class = treeLossSerializer
    filter_backends = (DjangoFilterBackend,)

    @action(detail=False, methods=["get"])
    def losses_within(self, request):
        longitude = request.GET.get("lng", None)
        latitude = request.GET.get("lat", None)

        if longitude and latitude:
            user_location = Point(float(longitude), float(latitude), srid=4326)
            buffer_distance = D(km=50)
            #buffer_geometry = user_location.buffer(buffer_distance)
            closest_nursery = TreeLoss.objects.filter(
                geom__distance_lte=(user_location, D(km=5))
                # geom__intersects=buffer_geometry
            )
            serializer = self.get_serializer_class()
            serialized_species = serializer(closest_nursery, many=True)
            return Response(serialized_species.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["get"])
    def losses_gee(self, request):
        longitude = request.GET.get("lng", None)
        latitude = request.GET.get("lat", None)

        if longitude and latitude:
           Map = geemap.Map(center=[longitude, latitude], zoom=4)


           Map.setCenter(longitude, latitude, 5)
           fc = ee.FeatureCollection('TIGER/2018/States').filter(ee.Filter.eq('STUSPS', 'MN'))

            # Create a Landsat 7, median-pixel composite for Spring of 2000.
           collection = ee.ImageCollection('LE7_L1T').filterDate("2000-05-01", "2000-10-31")
           image1 = collection.median()
            # Map.addLayer(image1)

            # # Clip to the output image to the California state boundary.
            # # fc = (ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8')
            # #       .filter(ee.Filter().eq('Name', 'Minnesota')))


           image2 = image1.clipToCollection(fc)

            # Select the red, green and blue bands.
           image = image2.select('B4', 'B3', 'B2')
           Map.addLayer(image, {'gain': [1.4, 1.4, 1.1]}, 'Landsat 7')

            # Display the map.
           return Map
            #return Response(serialized_species.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
