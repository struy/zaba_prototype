from django.contrib import admin

from .models import Promote, Banner, Area


class BannerInline(admin.TabularInline):
    model = Banner
    extra = 5


class PromoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [BannerInline]


admin.site.register(Promote, PromoteAdmin)
admin.site.register(Area)
