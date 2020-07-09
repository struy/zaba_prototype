import django_filters
from django.utils.translation import gettext_lazy as _
from .models import Item


class ItemsFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(label=_("Price is greater than"), lookup_expr='price__gt')
    price__lt = django_filters.NumberFilter(label=_("Price is less than"), lookup_expr='price__lt')

    class Meta:
        model = Item
        fields = {
            'price': ['gt', 'lt'],
            'condition': ['exact'],
            'city': ['exact']
        }
