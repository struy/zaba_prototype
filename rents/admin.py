from django.contrib import admin
from .models import Rental, RentalType
from modeltranslation.admin import TranslationAdmin


class RentalAdmin(TranslationAdmin):
    pass


# admin.site.unregister(RentalType)
admin.site.register(RentalType, RentalAdmin)
admin.site.register(Rental)
