import datetime
import redis

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import to_locale, get_language
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return f'media/{instance.__class__.__name__}/{instance.owner.id}_{filename}'


class AdvertsManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(description__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Advert(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name=_('owner'))
    expires = models.DateField(blank=True, null=True, help_text=_('Format mm/dd/yyyy'),
                               verbose_name=_('expires'))

    LOCALES = (('en', 'en_US'),
               ('uk', 'uk_UA'),
               ('ru', 'ru_RU'),
               ('pl', 'pl_PL'),
               )

    local = models.CharField(
        max_length=2,
        choices=LOCALES,
        default='en'
    )

    objects = AdvertsManager()

    class Meta:
        ordering = ['modified']
        abstract = True

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        lang = get_language()
        if lang:
            self.local = lang[:2]
        super(Advert, self).save(*args, **kwargs)

        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB)
        if (self.modified - self.created).seconds == 0:
            r.incr(f'Total:saved')
            r.incr(f'{self.__class__.__name__}:{self.id}:saved')
            data = self.created.timestamp()
            score = f'{self.__class__.__name__}:{self.created.timestamp()}'
            r.zadd("adverts", {score: data})

    def delete(self, using=None, keep_parents=False):
        r = redis.StrictRedis(host=settings.REDIS_HOST,
                              port=settings.REDIS_PORT,
                              db=settings.REDIS_DB)
        super(Advert, self).delete()
        r.decr(f'Total:saved')
        r.decr(f'{self.__class__.__name__}:{self.id}:saved')
        data = self.created.timestamp()
        score = f'{self.__class__.__name__}:{self.created.timestamp()}'
        r.zadd("adverts", {score: data})

    def __str__(self):
        return self.title


class Location(models.Model):
    city = models.CharField(max_length=50, default='Chicago', verbose_name=_('city'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    point = PointField(blank=True, verbose_name=_('map'), null=True)

    # zipcode =

    @property
    def lat_lng(self):
        return list(getattr(self.point, 'coords', [])[::-1])

    class Meta:
        ordering = ['city']
        abstract = True

    def __unicode__(self):
        return self.city

    def __str__(self):
        return self.city
