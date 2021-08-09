from django.contrib import admin

from .forms import BannerForm
from .models import Promote, Banner, Area


class BannerInline(admin.TabularInline):
    model = Banner
    form = BannerForm
    extra = 5


class PromoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]
    inlines = [BannerInline]


admin.site.register(Promote, PromoteAdmin)
admin.site.register(Area)
