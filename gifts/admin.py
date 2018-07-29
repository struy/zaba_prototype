from django.contrib import admin

from .models import GiftsType, Gift
from modeltranslation.admin import TranslationAdmin


class GiftsTypeAdmin(TranslationAdmin):
    list_display = ('name',)

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(GiftsType, GiftsTypeAdmin)
admin.site.register(Gift)