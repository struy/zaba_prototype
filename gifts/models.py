from django.db import models
from django.urls import reverse
from adverts.models import Advert, Location
from django.utils.translation import gettext_lazy as _


class GiftType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gift(Advert, Location):
    """
    handmade
    free classes
    free ticket
    volantir
    pet
    items
    """
    gift_type = models.ForeignKey(GiftType, on_delete=models.CASCADE, verbose_name=_('gift type'))
    image = models.ImageField(upload_to='gifts', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('gifts:detail', args=[self.id])
