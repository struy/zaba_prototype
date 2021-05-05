import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Item


class ItemsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    # TODO   price = django_filters.RangeFilter()
    # TODO django_filters/widgets/multiwidget.html

    class Meta:
        model = Item
        fields = {
            'price': ['gte', 'lte'],
            'condition': ['exact'],
            'city': ['exact']
        }
