from django.contrib import admin
from .models import Rental, PropertyType
from modeltranslation.admin import TranslationAdmin


class RentalAdmin(TranslationAdmin):
    pass


# admin.site.unregister(RentalType)
admin.site.register(PropertyType, RentalAdmin)
admin.site.register(Rental)
