from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Job, JobType


class JobAdmin(TranslationAdmin):
    pass


admin.site.unregister(JobType)
admin.site.register(JobType, JobAdmin)
admin.site.register(Job)
