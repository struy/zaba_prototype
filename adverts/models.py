import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)


class Advert(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # default = (timezone.now().date() - datetime.timedelta(days=7))
    expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['modified']
        abstract = True

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.title


class Location(models.Model):
    city = models.CharField(max_length=42, default='Chicago')
    neighborhoods = models.CharField(max_length=42, blank=True)

    class Meta:
        ordering = ['city']

    def __unicode__(self):
        return self.city

    def __str__(self):
        return self.city
