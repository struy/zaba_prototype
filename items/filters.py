import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Item
from django.contrib.postgres.fields import IntegerRangeField


class ItemsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    # price__gte = django_filters.NumberFilter(label=_("Price is greater than"), lookup_expr='price__gte')
    # price__lte = django_filters.NumberFilter(label=_("Price is less than"), lookup_expr='price__lte')
    # TODO   price = django_filters.RangeFilter()
    # TODO django_filters/widgets/multiwidget.html

    class Meta:
        model = Item
        fields = {
            'price': ['gte', 'lte'],
            'condition': ['exact'],
            'city': ['exact']
        }

