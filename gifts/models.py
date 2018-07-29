from django.db import models
from adverts.models import Advert



class GiftsType(models.Model):
    name = models.CharField(max_length=42)


class Gift(Advert):
    """
    handmade
    free classes
    free ticket
    volantir
    pet
    items
    """
    gifts_type = models.ForeignKey(GiftsType, on_delete=models.CASCADE)


