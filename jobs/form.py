from django import forms
from django.contrib.gis import forms as gis_forms
from django_countries.widgets import CountrySelectWidget
from jobs.models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "jobtype",
            "description",
            "salary",
            "address",
            "city",
            "duration",
            "expires",
            "point",
            "countries",
        ]
        widgets = dict(expires=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
                       point=gis_forms.OSMWidget(attrs={'default_lon': -88, 'default_lat': 41.9, 'map_width': 800,
                                                        'map_height': 500, 'default_zoom': 10}),
                       )
