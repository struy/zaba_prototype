import django_filters

from .models import Item


class ItemsFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = {
            'price': ['gt', 'lt'],
            'condition': ['exact'],
            'city': ['exact']
        }
