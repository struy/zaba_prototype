from modeltranslation.translator import translator, TranslationOptions
from .models import RentalType


class RentalsTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(RentalType, RentalsTypeTranslationOptions)
