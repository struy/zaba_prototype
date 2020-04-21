from django.contrib import admin
from .models import Job, JobType
from modeltranslation.admin import TranslationAdmin


class JobAdmin(TranslationAdmin):
    pass


admin.site.unregister(JobType)
admin.site.register(JobType, JobAdmin)
admin.site.register(Job)
