from django.contrib.gis import admin
from .models import Event, Counties

admin.site.register(Event, admin.OSMGeoAdmin)
admin.site.register(Counties, admin.OSMGeoAdmin)

