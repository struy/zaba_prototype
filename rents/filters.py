import django_filters
from django.db import models
from django import forms

from .models import Rental


class RentsFilter(django_filters.FilterSet):

    class Meta:
        model = Rental
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
