from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Rental, PropertyType


class RentalAdmin(TranslationAdmin):
    pass


admin.site.register(PropertyType, RentalAdmin)
admin.site.register(Rental)
