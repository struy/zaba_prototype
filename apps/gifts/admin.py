from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from apps.gifts.models import GiftType, Gift


class GiftTypeAdmin(TranslationAdmin):
    pass


admin.site.register(GiftType, GiftTypeAdmin)
admin.site.register(Gift)
