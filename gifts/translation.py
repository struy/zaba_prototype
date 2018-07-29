from modeltranslation.translator import translator, TranslationOptions
from gifts.models import GiftsType


class GiftsTypeTranslationOptions(TranslationOptions):
    """
    Класс настроек интернационализации полей модели Modelka.
    """

    fields = ('name',)


translator.register(GiftsType, GiftsTypeTranslationOptions)
