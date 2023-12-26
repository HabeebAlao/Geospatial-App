from django.contrib.gis import admin
from .models import eds,counties

admin.site.register(eds, admin.ModelAdmin)
admin.site.register(counties, admin.ModelAdmin)
