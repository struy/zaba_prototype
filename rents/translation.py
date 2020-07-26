from modeltranslation.translator import translator, TranslationOptions
from .models import PropertyType


class PropertyTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(PropertyType, PropertyTypeTranslationOptions)
