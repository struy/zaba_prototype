from modeltranslation.translator import translator, TranslationOptions
from apps.gifts.models import GiftType


class GiftsTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(GiftType, GiftsTypeTranslationOptions)
