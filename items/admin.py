from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Item


@admin.register(Item)
class ItemAdmin(OSMGeoAdmin):
    """
    OSMGeoAdmin
    With the OSMGeoAdmin, GeoDjango uses a Open Street Map layer in the admin. This provides more context
    (including street and thoroughfare details) than available with the GeoModelAdmin (which uses the Vector Map
    Level 0 WMS dataset hosted at OSGeo).
    First, there are some important requirements:
    OSMGeoAdmin requires that GDAL is installed.
    The PROJ.4 datum shifting files must be installed (see the PROJ.4 installation instructions for more details).
    """

    default_lon = -9753402
    default_lat = 5140871
    default_zoom = 10
