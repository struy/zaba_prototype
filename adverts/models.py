import datetime
import redis

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.utils.text import slugify
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)
from django.utils.translation import gettext_lazy as _


class Advert(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name=_('owner'))
    expires = models.DateTimeField(blank=True, null=True, help_text=_('This is the help text'),
                                   verbose_name=_('expires'))

    class Meta:
        ordering = ['modified']
        abstract = True

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def get_image_filename(self, filename):
        slug = slugify(self.title)
        return "%s/%s/%s" % (self.__class__.__name__, slug, filename)

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
    city = models.CharField(max_length=50, default='Chicago', verbose_name=_('city'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    point = PointField(verbose_name=_('point'), blank=True)

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
