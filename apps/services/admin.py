from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Service, ServiceType


class ServiceTypeAdmin(TranslationAdmin):
    pass

class ServiceAdmin(admin.ModelAdmin):
    list_filter = ('local','service_type', 'city')


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
