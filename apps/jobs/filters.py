import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Job


class JobsFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(widget=forms.TextInput(attrs={'placeholder': _("Only Latin characters")}))

    class Meta:
        model = Job
        fields = {
            'per': ['exact'],
            'salary': ['gte', 'lte'],
            'jobtype': ['exact'],
            'city': ['exact']
        }

    # @property
    # def qs(self):
    #     per = getattr(self.request, 'per', None)
    #     if self.request and per:
    #         self.request['salary__gte'] *= 2000  # (50 weeks * 40 hours)
    #         self.request['salary__lte'] *= 2000
    #
    #     parent = super().qs
    #
    #     return parent
