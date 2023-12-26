from django.contrib.gis.db import models


class eds(models.Model):
    osm_id = models.FloatField(null=True, blank=True)
    name_tag = models.CharField(max_length=255, null=True, blank=True)
    name_ga = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    alt_name = models.CharField(max_length=255, null=True, blank=True)
    alt_name_g = models.CharField(max_length=255, null=True, blank=True)
    osm_user = models.CharField(max_length=100, null=True, blank=True)
    osm_timest = models.CharField(max_length=38, null=True, blank=True)
    attributio = models.CharField(max_length=255, null=True, blank=True)
    logainm_re = models.CharField(max_length=255, null=True, blank=True)
    co_name = models.CharField(max_length=255, null=True, blank=True)
    co_osm_id = models.FloatField(null=True, blank=True)
    t_ie_url = models.CharField(max_length=65, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    epoch_tstm = models.FloatField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True, blank=True)


# Auto-generated `LayerMapping` dictionary for eds model
eds_mapping = {
    'osm_id': 'OSM_ID',
    'name_tag': 'NAME_TAG',
    'name_ga': 'NAME_GA',
    'name_en': 'NAME_EN',
    'alt_name': 'ALT_NAME',
    'alt_name_g': 'ALT_NAME_G',
    'osm_user': 'OSM_USER',
    'osm_timest': 'OSM_TIMEST',
    'attributio': 'ATTRIBUTIO',
    'logainm_re': 'LOGAINM_RE',
    'co_name': 'CO_NAME',
    'co_osm_id': 'CO_OSM_ID',
    't_ie_url': 'T_IE_URL',
    'area': 'AREA',
    'latitude': 'LATITUDE',
    'longitude': 'LONGITUDE',
    'epoch_tstm': 'EPOCH_TSTM',
    'geom': 'MULTIPOLYGON',
}


class counties(models.Model):
    osm_id = models.FloatField()
    name_tag = models.CharField(max_length=255)
    name_ga = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255)
    alt_name_g = models.CharField(max_length=255)
    logainm_re = models.CharField(max_length=255)
    osm_user = models.CharField(max_length=100)
    osm_timest = models.CharField(max_length=38)
    attributio = models.CharField(max_length=255)
    t_ie_url = models.CharField(max_length=35)
    area = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    epoch_tstm = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)


# Auto-generated `LayerMapping` dictionary for counties model
counties_mapping = {
    'osm_id': 'OSM_ID',
    'name_tag': 'NAME_TAG',
    'name_ga': 'NAME_GA',
    'name_en': 'NAME_EN',
    'alt_name': 'ALT_NAME',
    'alt_name_g': 'ALT_NAME_G',
    'logainm_re': 'LOGAINM_RE',
    'osm_user': 'OSM_USER',
    'osm_timest': 'OSM_TIMEST',
    'attributio': 'ATTRIBUTIO',
    't_ie_url': 'T_IE_URL',
    'area': 'AREA',
    'latitude': 'LATITUDE',
    'longitude': 'LONGITUDE',
    'epoch_tstm': 'EPOCH_TSTM',
    'geom': 'MULTIPOLYGON',
}
