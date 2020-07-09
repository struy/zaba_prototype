import django_filters
from django.utils.translation import gettext_lazy as _

from .models import Item


class ItemsFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['gt', 'lt'],
            'condition': ['exact'],
            'city': ['exact']
        }