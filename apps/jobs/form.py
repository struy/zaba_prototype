from django import forms
from django.contrib.gis import forms as gis_forms
from django.utils.translation import gettext_lazy as _

from apps.jobs.models import Job


class JobForm(forms.ModelForm):
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))
    salary = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': _("per hour / per mile")}))

    class Meta:
        model = Job
        fields = [
            "title",
            "jobtype",
            "description",
            "image",
            "address",
            "city",
            "duration",
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
