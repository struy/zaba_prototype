import django_filters
from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from .models import Rent


class RentsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Rent
        fields = {
            'property_type': ['exact'],
            'prefer_sex': ['exact'],
            'pet_policy': ['exact'],
            'bathrooms': ['exact'],
            'bedrooms': ['exact'],
            'price': ['gte', 'lte'],
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
