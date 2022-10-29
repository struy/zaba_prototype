from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Service, ServiceType


class ServiceAdmin(TranslationAdmin):
    pass


admin.site.register(Service)
admin.site.register(ServiceType, ServiceAdmin)
