from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.adverts.models import Advert, Location, user_directory_path


class GiftType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gift(Advert, Location):
    """
    handmade
    free classes
    free ticket
    volunteering
    pet
    items
    """
    gift_type = models.ForeignKey(GiftType, on_delete=models.CASCADE, verbose_name=_('gift type'))
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    favourites = models.ManyToManyField(User, related_name='favourite_gifts', default=None, blank=True)

    @property
    def icon_path(self):
        if self.gift_type == 'pets':
            return f'none/gifts/none-pets.svg'
        else:
            return f'none/gifts/none-free.svg'

    def get_absolute_url(self):
        return reverse('gifts:detail', args=[self.id])

    def get_api_fav_url(self):
        return reverse('favourite_add', kwargs={'name': 'Gift', 'record_id': self.id})

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
