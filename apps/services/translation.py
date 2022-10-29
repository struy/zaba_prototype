from modeltranslation.translator import translator, TranslationOptions

from apps.services.models import ServiceType


class ServiceTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(ServiceType, ServiceTypeTranslationOptions)
