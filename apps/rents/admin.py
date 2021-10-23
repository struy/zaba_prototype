from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Rent, PropertyType


class RentalAdmin(TranslationAdmin):
    pass


admin.site.register(PropertyType, RentalAdmin)
admin.site.register(Rent)
