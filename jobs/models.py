from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from adverts.models import Advert, Location
from django.utils.translation import gettext_lazy as _


class JobType(models.Model):
    name = models.CharField(max_length=42)

    def __str__(self):
        return self.name


class Job(Advert, Location):
    """
    :type
    duration
    payment
    """
    jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_('job type'))
    DURATIONS = (('ft', _('full-time')),
                 ('pt', _('part-time')),
                 ('ca', _('casual')),)
    duration = models.CharField(
        max_length=2,
        choices=DURATIONS,
        default='ft'
    )
    countries = CountryField(multiple=True, default='EN', verbose_name=_('language'), help_text=_('What language does the employer speak?'),)
    salary = models.PositiveIntegerField(blank=True, verbose_name=_('salary'))

    def get_absolute_url(self):
        return reverse('jobs:detail', args=[self.id])
