from django.contrib import admin
from apps.jobs.models import JobType


class ListAdmin(admin.ModelAdmin):
    fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


admin.site.register([JobType])
