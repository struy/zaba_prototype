from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField

from apps.adverts.models import Advert, Location, user_directory_path
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField


class JobType(models.Model):
    name = models.CharField(max_length=42)
    icon = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Job(Advert, Location):
    """
    :type
    duration
    payment
    LOGO
    """
    DURATIONS = (('ft', _('full-time')),
                 ('pt', _('part-time')),
                 ('ca', _('casual')),)

    jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_('job type'))
    duration = models.CharField(
        max_length=2,
        choices=DURATIONS,
        default='ft'
    )
    countries = CountryField(multiple=True, default='EN', verbose_name=_('language'),
                             help_text=_('What language does the employer speak?'), )
    image = ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name=_('Logo or image'))
    favourites = models.ManyToManyField(User, related_name='favourite_jobs', default=None, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('salary'), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('jobs:detail', args=[self.id])

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
