from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import ImageField

from apps.adverts.models import Advert, Location, user_directory_path


class Item(Advert, Location):
    """ Items for sale """
    CONDITIONS = [('0', _('Used')),
                  ('1', _('Acceptable')),
                  ('2', _('Very Good')),
                  ('3', _('Like New')),
                  ('4', _('New')),
                  ]
    condition = models.CharField(
        max_length=1,
        choices=CONDITIONS,
        default='0',
        verbose_name=_('condition')
    )
    image = ImageField(upload_to=user_directory_path, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'))
    favourites = models.ManyToManyField(User, related_name='favourite_items', default=None, blank=True)

    def get_absolute_url(self):
        return reverse('items:detail', args=[self.id])

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
