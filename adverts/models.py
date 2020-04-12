import datetime
import redis

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)


class Advert(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['modified']
        abstract = True

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        super(Advert, self).save(*args, **kwargs)
        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB)
        if (self.modified - self.created).seconds == 0:
            r.incr(f'Total:saved')
            r.incr(f'{self.__class__.__name__}:{self.id}:saved')

    def delete(self, using=None, keep_parents=False):
        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB)
        super(Advert, self).delete()
        r.decr(f'Total:saved')
        r.decr(f'{self.__class__.__name__}:{self.id}:saved')

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
