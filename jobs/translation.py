from modeltranslation.translator import translator, TranslationOptions
from jobs.models import JobType


class JobsTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(JobType, JobsTypeTranslationOptions)
