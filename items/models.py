from django.db import models
from adverts.models import Advert, Location


# Create your models here.
class Item(Advert):
    # condition =
    # size =
    price = models.PositiveIntegerField()

