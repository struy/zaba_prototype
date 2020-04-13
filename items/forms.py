from django import forms
from django.contrib.gis import forms as gis_forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'expires', 'city', 'address', 'point', 'price']
        widgets = {
            'expires': forms.SelectDateWidget(),
            'point': gis_forms.OSMWidget(attrs={'default_lon': 20, 'default_lat': 30}),
        }
