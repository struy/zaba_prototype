import django_tables2 as tables
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.adverts.models import Advert, Location, user_directory_path


class PropertyType(models.Model):
    name = models.CharField(max_length=42)

    def __str__(self):
        return self.name


class Rental(Advert, Location):
    """
    Move-in Date
    Type : apartments, houses, condos, townhouses, basement
    Та́ун-ха́ус,
    bedrooms : studio, 1,2,3,4+
    bathrooms 1,2,3+
    """
    # TODO Available

    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, verbose_name=_('property type'))
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    favourites = models.ManyToManyField(User, related_name='favourite_rents', default=None, blank=True)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    bedrooms = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()
    POLICES = ((0, _('None')),
               (1, _('Dogs')),
               (2, _('Cats')),
               (3, _('Dogs and Cats')),
               (4, _('Any')),
               )
    pet_policy = models.PositiveSmallIntegerField(
        choices=POLICES,
        default=0
    )
    furnished = models.BooleanField()
    prefer_sex_list = (('a', _('any')),
                       ('w', _('woman')),
                       ('m', _('man')),
                       )

    prefer_sex = models.CharField(
        max_length=1,
        choices=prefer_sex_list,
        default='a'
    )

    def get_absolute_url(self):
        return reverse('rents:detail', args=[self.id])

    def get_api_fav_url(self):
        return reverse('favourite_add', kwargs={'name': 'Rental', 'record_id': self.id})


class RentalTable(tables.Table):
    class Meta:
        model = Rental
