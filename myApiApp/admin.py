from django.contrib.gis import admin
from .models import eds,counties

admin.site.register(eds, admin.OSMGeoAdmin)
admin.site.register(counties, admin.OSMGeoAdmin)
