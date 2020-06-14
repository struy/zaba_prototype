from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Rental


class RentForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = '__all__'
        # ['title', 'description', 'price', 'image', 'expires', 'city', 'address', 'point']
        widgets = {
            'expires': forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
            'point': gis_forms.OSMWidget(attrs={'default_lon': 20, 'default_lat': 30, 'map_width': 800,
                                                'map_height': 500, }),
        }

