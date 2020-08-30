import django_filters
from .models import Job


class JobsFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = {
            'salary': ['gte', 'lte'],
            'jobtype': ['exact'],
            'city': ['exact']
        }
