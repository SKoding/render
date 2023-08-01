from rest_framework_gis import serializers
from rest_framework import serializers as serial
from .models import Administration, chiefs, treeSpecies, treeNursery, TreeLoss

#Administration
class adminSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = Administration
        fields = ('gid','name_4')
        geo_field = "geom"

class chiefSerializer(serial.Serializer):
    class Meta:
        model = chiefs
        fields = ('__all__')

class speciesSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = treeSpecies
        fields = ('gid','soiltextur','elevation','rainfallto','species')
        geo_field = "geom"

class treeNuserySerializer(serializers.GeoFeatureModelSerializer):	
	#distance = serial.SerializerMethodField()
	class Meta:
		model = treeNursery
		fields = '__all__'
		geo_field = 'geom'
		#read_only_fields = ['distance']

class treeLossSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        model = TreeLoss
        fields = ('__all__')
        geo_field = 'geom'