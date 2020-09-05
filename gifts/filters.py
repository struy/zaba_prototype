import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _


from .models import Gift


class GiftsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Gift
        fields = {
            'gift_type': ['exact'],
            'city': ['exact']
        }
