from django.contrib.gis import admin
from .models import Event

admin.site.register(Event, admin.ModelAdmin)
