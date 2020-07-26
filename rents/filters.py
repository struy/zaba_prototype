import django_filters
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms

from .models import Rental


class RentsFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(label=_("Price is greater than"), lookup_expr='price__gt')
    price__lt = django_filters.NumberFilter(label=_("Price is less than"), lookup_expr='price__lt')

    class Meta:
        model = Rental
        fields = {
            'property_type': ['exact'],
            'prefer_sex': ['exact'],
            'pet_policy': ['exact'],
            'bathrooms': ['exact'],
            'bedrooms': ['exact'],
            'price': ['gt', 'lt'],
            'city': ['exact'],
            'furnished': ['exact']

        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            }
        }
