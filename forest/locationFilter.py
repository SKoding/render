##src/gis_rest_project/nairobi_hospitals_api/hospitals_filters.py
from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import treeNursery, Administration

class treeNuseriesFilter(GeoFilterSet):
    location = filters.CharFilter(method= 'get_facilities_by_location')


    class Meta:
        model = treeNursery
        exclude = ['geom']

    def get_facilities_by_location(self, queryset, name, value ):
        query_ = Administration.objects.filter(pk=value)
        if query_:
            obj = query_.first()
            return queryset.filter(geom__intersects = obj.geom)
        return queryset