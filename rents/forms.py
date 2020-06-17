from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Rental


class RentForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['rental_type', 'title', 'description', 'expires', 'price', 'image', 'pet_policy',
                  'bathrooms', 'bedrooms', 'furnished', 'city', 'address', 'point']
        widgets = {
            'expires': forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
            'point': gis_forms.OSMWidget(attrs={'default_lon': -88, 'default_lat': 41.9, 'map_width': 800,
                                                'map_height': 500,'default_zoom': 10}),
        }

