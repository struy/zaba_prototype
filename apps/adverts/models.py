import datetime
from collections import namedtuple

import pytz
import redis
from django.conf import settings
# from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import (
    TitleSlugDescriptionModel, TimeStampedModel)


def user_directory_path(instance, filename):
    """ file will be uploaded to MEDIA_ROOT /<class_name>/<year>/<month>/<day>/user_<id>_<filename>"""
    now = datetime.datetime.now()
    return f'{instance.__class__.__name__}s/{now.year}/{now.month}/{now.day}/{instance.author.id}_{filename}'


def validate_expires(value):
    less_date = value - datetime.timedelta(days=1)
    more_date = value + datetime.timedelta(weeks=4)
    if value < less_date:
        raise ValidationError(
            _('%(value)s can\'t be past'),
            params={'value': value},
        )
    if value > more_date:
        raise ValidationError(
            _('%(value)s can\'t be more than month'),
            params={'value': value},
        )


class AdvertsManager(models.Manager):
    def search(self, query=None):
        lang = get_language()
        local = None
        if lang:
            local = lang[:2]
        qs = self.get_queryset()
        if query is not None:
            if local is not None:
                or_lookup = (Q(local__exact=local) & (Q(title__icontains=query) | Q(description__icontains=query)))
            else:
                or_lookup = (Q(title__icontains=query) | Q(description__icontains=query))
            qs = qs.filter(or_lookup).distinct()  # distinct() is often necessary with Q lookups
        return qs


class Advert(TitleSlugDescriptionModel, TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name=_('author'))
    expires = models.DateField(blank=True, null=True, help_text=_('Format mm/dd/yyyy'),
                               verbose_name=_('expires'), validators=[validate_expires])

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

    @property
    def expires_type(self):
        """ return namedtuple(css, text) or None"""
        utc = pytz.UTC
        now = utc.localize(datetime.datetime.today())
        NT = namedtuple('NT', 'css text')
        if (self.modified + datetime.timedelta(weeks=2)) > now:
            return NT("px-1 text-white bg-success", _("new"))
        if (self.modified + datetime.timedelta(weeks=4)) > now:
            return None
        if (self.modified + datetime.timedelta(weeks=12)) > now:
            return NT("px-1 text-white bg-secondary", _("old"))
        if (self.modified + datetime.timedelta(weeks=24)) > now:
            return NT("px-1 text-white bg-secondary", _("very old"))
        return NT("px-1 text-white bg-dark", _("dead"))

    objects = AdvertsManager()

    class Meta:
        ordering = ['modified']
        abstract = True

    def was_published_recently(self):
        return self.created >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        lang = get_language()
        # TODO admin save with local
        if lang:
            self.local = lang[:2]
        super(Advert, self).save(*args, **kwargs)

        r = redis.Redis(connection_pool=settings.POOL)

        if (self.modified - self.created).seconds == 0:
            r.incr('Total:saved')
            r.incr(f'{self.__class__.__name__}:{self.id}:saved')
            r.lpush(f'{self.__class__.__name__}:new', self.id)
            r.ltrim(f'{self.__class__.__name__}:new', 0, 12)
            data = self.created.timestamp()
            score = f'{self.__class__.__name__}:{self.created.timestamp()}'
            r.zadd("adverts", {score: data})

    def delete(self, using=None, keep_parents=False):
        r = redis.Redis(connection_pool=settings.POOL)
        super(Advert, self).delete()
        r.decr('Total:saved')
        r.decr(f'{self.__class__.__name__}:{self.id}:saved')
        data = self.created.timestamp()
        score = f'{self.__class__.__name__}:{self.created.timestamp()}'
        r.zadd("adverts", {score: data})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Location(models.Model):
    city = models.CharField(max_length=50, default='Chicago', verbose_name=_('city'))
    address = models.CharField(max_length=100, blank=True, verbose_name=_('address'))
    point = PointField(geography=True, verbose_name=_('map'), null=True, blank=True)

    # zipcode =

    @property
    def lat_lng(self):
        """for ubuntu 20.04(GDAL v. 3) dont need use revers
         getattr(self.point, 'coords', [])[::-1]
         """
        return list(getattr(self.point, 'coords', []))

    class Meta:
        ordering = ['city']
        abstract = True

    def __unicode__(self):
        return self.city

    def __str__(self):
        return self.city
