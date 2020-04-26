from django.db import models
from django.utils.translation import gettext_lazy as _
import django_tables2 as tables
from adverts.models import Advert, Location


class RentalType(models.Model):
    name = models.CharField(max_length=42)

    def __str__(self):
        return self.name


class Rental(Advert, Location):
    # bedrooms : studio, 1,2 3+
    # Rooms, Apartment
    # Move-in Date

    rental_type = models.ForeignKey(RentalType, on_delete=models.CASCADE, verbose_name=_('job type'))

    bathrooms = models.PositiveSmallIntegerField(default=1)
    bedrooms = models.PositiveSmallIntegerField(default=2)
    price = models.PositiveIntegerField()
    POLICES = (('0', 'None'),
               ('1', 'Dogs'),
               ('2', 'Cats'),
               ('3', 'Dogs adn Cats'),
               ('4', 'Any'),
               )
    pet_policy = models.CharField(
        max_length=1,
        choices=POLICES,
        default='1'
    )
    furnished = models.BooleanField()
    prefer_sex_list = (('a', 'any'),
                       ('w', 'woman'),
                       ('m', 'man'),
                       )
    prefer_sex = models.CharField(
        max_length=1,
        choices=prefer_sex_list,
        default='a'
    )


class RentalTable(tables.Table):
    class Meta:
        model = Rental
