from django import forms
from django.contrib.gis import forms as gis_forms
from jobs.models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "address",
            "city",
            "description",
            "duration",
            "expires",
            "jobtype",
            "point",
            "salary",
            "title"
        ]
        widgets = dict(expires=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
                       point=gis_forms.OSMWidget(attrs={'default_lon': 20, 'default_lat': 30, 'map_width': 800,
                                                        'map_height': 500, }))
