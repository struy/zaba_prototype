from django import forms
from django.contrib.gis import forms as gis_forms
from gifts.models import Gift


class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['gift_type', 'title', 'description', 'image', 'expires', 'city', 'address', 'point' ]
        widgets = dict(expires=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
                       point=gis_forms.OSMWidget(attrs={'default_lon': -88, 'default_lat': 41.9, 'map_width': 800,
                                                        'map_height': 500, 'default_zoom': 10}))
