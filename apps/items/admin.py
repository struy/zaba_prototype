from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Item


@admin.register(Item)
class ItemAdmin(OSMGeoAdmin):
    ordering = ('-modified',)
    default_lon = -9753402
    default_lat = 5140871
    default_zoom = 10
    search_fields = ['title', 'description']
