from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'expires', 'price', 'city', 'address', 'point']
        widgets = {
            'expires': forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
            'point': gis_forms.OSMWidget(attrs={'default_lon': 20, 'default_lat': 30, 'map_width': 800,
                                                'map_height': 500, }),
        }
