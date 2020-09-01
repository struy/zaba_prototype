from django import forms
from django.contrib.gis import forms as gis_forms
from jobs.models import Job


class JobForm(forms.ModelForm):
    expires = forms.DateField(
        localize=True,
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
    )

    class Meta:
        model = Job
        fields = [
            "title",
            "jobtype",
            "description",
            "image",
            "salary",
            "address",
            "city",
            "duration",
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
