from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from sorl.thumbnail import ImageField

from apps.adverts.models import Advert, Location, user_directory_path


class Service(Advert, Location):
    """
    """
    # jobtype = models.ForeignKey(JobType, on_delete=models.CASCADE, verbose_name=_('service type'))
    countries = CountryField(multiple=True, default='EN', verbose_name=_('language'),
                             help_text=_('What language do we speak?'), )
    image = ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name=_('Logo or image'))
    favourites = models.ManyToManyField(User, related_name='favourite_services', default=None, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('salary'), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('services:detail', args=[self.id])

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
