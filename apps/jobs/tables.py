import django_tables2 as tables

from .models import Job


class JobTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Job
        fields = ('city', 'title', 'jobtype', 'salary')
