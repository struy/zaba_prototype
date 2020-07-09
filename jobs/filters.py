import django_filters
from django.utils.translation import gettext_lazy as _
from .models import Job


class JobsFilter(django_filters.FilterSet):
    salary__gt = django_filters.NumberFilter(label=_("Salary is greater than"), lookup_expr='salary__gt')
    salary__lt = django_filters.NumberFilter(label=_("Salary is less than"), lookup_expr='salary__lt')

    class Meta:
        model = Job
        fields = {
            'salary': ['gt', 'lt'],
            'jobtype': ['exact'],
            'city': ['exact']
        }
