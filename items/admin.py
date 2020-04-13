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

3785 is old and was replaced by 900913 ('google') which was then replaced by 3857.

    from django.contrib.gis.geos import Point
    center = Point((41.87, -87.61), srid=4326)
    center.transform(3785)
    center.y
    -24682980.487229597
    center.x
    4660947.079514365
    """
    default_lon = 4660947
    default_lat = -24682980
    default_zoom = 12
