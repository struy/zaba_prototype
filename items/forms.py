from django import forms
from django.contrib.gis import forms as gis_forms
from django_select2 import forms as s2forms
# from cities_light.models import City
from .models import Item


class CityWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "city__icontains",
    ]


class ItemForm(forms.ModelForm):
    expires = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Item
        fields = ['condition', 'title', 'description', 'price', 'image', 'expires', 'city', 'address', 'point']
        widgets = {
            'point': gis_forms.OSMWidget(attrs={
                'default_lon': -88,
                'default_lat': 41.9,
                'map_width': 800,
                'map_height': 500,
                'default_zoom': 10,
            }),
            'city': CityWidget
        }
