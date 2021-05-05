from django.contrib import admin

from apps.gifts.models import GiftType, Gift
from modeltranslation.admin import TranslationAdmin


class GiftTypeAdmin(TranslationAdmin):
    pass


admin.site.register(GiftType, GiftTypeAdmin)
admin.site.register(Gift)
