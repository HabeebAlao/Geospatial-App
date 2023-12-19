from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    address = models.CharField(max_length=255, null=True, blank=True)
    location = models.PointField()
    going_users = models.ManyToManyField(User, related_name='going_events', blank=True)

    def __str__(self):
        return self.event_name


class Counties(models.Model):
    osm_id = models.FloatField()
    name_tag = models.CharField(max_length=255, null=True, blank=True)
    name_ga = models.CharField(max_length=255, null=True, blank=True)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    alt_name = models.CharField(max_length=255, null=True, blank=True)
    alt_name_g = models.CharField(max_length=255, null=True, blank=True)
    logainm_re = models.CharField(max_length=255, null=True, blank=True)
    osm_user = models.CharField(max_length=100, null=True, blank=True)
    osm_timest = models.CharField(max_length=38, null=True, blank=True)
    attributio = models.CharField(max_length=255, null=True, blank=True)
    t_ie_url = models.CharField(max_length=35, null=True, blank=True)
    area = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    epoch_tstm = models.FloatField(null=True, blank=True)
    geom = models.MultiPolygonField(srid=4326, null=True, blank=True)


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
