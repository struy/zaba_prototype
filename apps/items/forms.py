from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.translation import gettext_lazy as _

from .models import Item


class ItemForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Item
        fields = ['condition',
                  'title',
                  'description',
                  'price',
                  'image',
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
