from django.contrib import admin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Advert, Location
from jobs.models import JobType


class ListAdmin(admin.ModelAdmin):
    fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


# class CityAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.PointField: {"widget": GooglePointFieldWidget}
#     }


admin.site.register([Location, JobType])
