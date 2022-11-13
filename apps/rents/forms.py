from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.translation import gettext_lazy as _

from .models import Rent


class RentForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Rent
        fields = ['property_type',
                  'title',
                  'description',
                  'price',
                  'image',
                  'pet_policy',
                  'bathrooms',
                  'bedrooms',
                  'furnished',
                  'city',
                  'address',
                  'point']
        widgets = {
            'point': gis_forms.OSMWidget(attrs={
                'default_lon': -88,
                'default_lat': 41.9,
                'map_width': 800,
                'map_height': 500,
                'default_zoom': 10,
            }),
        }
