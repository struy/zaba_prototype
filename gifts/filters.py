import django_filters

from .models import Gift


class GiftsFilter(django_filters.FilterSet):
    class Meta:
        model = Gift
        fields = {
            'gift_type': ['exact'],
            'city': ['exact']
        }
