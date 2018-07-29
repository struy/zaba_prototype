from django.db import models
# from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

# Create your models here.
from adverts.models import Advert, Location
import django_tables2 as tables



class Rental(Advert):
    # bedroooms : studio, 1,2 3+
    # Rooms, Apartment
    # Map

    bathrooms = models.PositiveSmallIntegerField(default=1)
    bedrooms = models.PositiveSmallIntegerField(default=2)
    price = models.PositiveIntegerField()
    POLICE = (('1', 'None'),
              ('2', 'Dogs'),
              ('3', 'Cats'),
              ('4', 'Dogs adn Cats'),
              ('5', 'Any'),
              )
    pet_policy = models.CharField(
        max_length=1,
        choices=POLICE,
        default='1'
    )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    furnished = models.BooleanField()
    prefer_sex_list = (('a', 'any'),
                       ('g', 'woman'),
                       ('b', 'man'),
                       )
    prefer_sex = models.CharField(
        max_length=1,
        choices=prefer_sex_list,
        default='a'
    )
    attached = models.ImageField(
        upload_to='media/rents',
        max_length=1000,
        verbose_name='Imagen',
        null=True,
        blank=True

    )
    address = models.TextField()
    # coordinates = models.PointField() #https://github.com/erdem/django-map-widgets


class RentalTable(tables.Table):
    class Meta:
        model = Rental