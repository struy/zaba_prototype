from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from sorl.thumbnail import ImageField

from apps.adverts.models import Advert, Location, user_directory_path


class ServiceType(models.Model):
    name = models.CharField(max_length=42)
    icon = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Service(Advert, Location):
    """
    Temporary  Service advertise, example Sales
    """
    countries = CountryField(multiple=True, default='EN', verbose_name=_('language'),
                             help_text=_('What language do we speak?'), )
    image = ImageField(upload_to=user_directory_path, null=True, blank=True, verbose_name=_('Logo or image'))
    favourites = models.ManyToManyField(User, related_name='favourite_services', default=None, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, verbose_name=_('service type'), default="")

    @property
    def icon_path(self):
        return f'none/services/none-services.svg'

    def get_absolute_url(self):
        return reverse('services:detail', args=[self.id])

    def get_api_fav_url(self):
        return reverse('favourite_add', kwargs={'name': 'Service', 'record_id': self.id})

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
