from datetime import datetime, timedelta
from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.translation import gettext_lazy as _

from .models import Service


class ServiceForm(forms.ModelForm):
    expires = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d',
                               attrs={'type': 'date',
                                      'min': datetime.now().strftime("%Y-%m-%d"),
                                      'max': (datetime.now() + timedelta(weeks=2)).strftime("%Y-%m-%d")
                                      }),
    )
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Service
        fields = [
            "title",
            "description",
            "image",
            "salary",
            "address",
            "city",
            "expires",
            "point",
            "countries",
        ]
        widgets = {
            'point': gis_forms.OSMWidget(attrs={
                'default_lon': -88,
                'default_lat': 41.9,
                'map_width': 800,
                'map_height': 500,
                'default_zoom': 10,
            }),
        }
