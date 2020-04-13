from django.db import models
from adverts.models import Advert, Location
from django.utils.translation import gettext_lazy as _


class Item(Advert, Location):
    # condition =
    # size =
    price = models.PositiveIntegerField(verbose_name=_('price'))
