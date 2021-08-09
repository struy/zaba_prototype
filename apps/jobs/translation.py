from modeltranslation.translator import translator, TranslationOptions

from apps.jobs.models import JobType


class JobsTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(JobType, JobsTypeTranslationOptions)
