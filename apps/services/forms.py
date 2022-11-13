from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.translation import gettext_lazy as _

from .models import Service, ServiceType


class ServiceForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))
    # TODO order by lang
    # service_type = forms.ModelChoiceField(queryset=ServiceType.objects.order_by(f'name<LANG>'))

    class Meta:
        model = Service
        fields = [
            "service_type",
            "title",
            "description",
            "image",
            "address",
            "city",
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
