##Sample serializer

from rest_framework_gis.serializers import GeoFeatureModelSerializer

from rest_framework import serializers

from .models import eds, counties


class ElectoralDistrictsSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = eds

        fields = '__all__'

        geo_field = 'geom'


class CountiesSerializer(GeoFeatureModelSerializer):
    distance = serializers.CharField()

    class Meta:
        model = counties

        fields = '__all__'

        geo_field = 'geom'
