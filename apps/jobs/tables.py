import django_tables2 as tables

from .models import Job


class JobTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_absolute_url}}">{{record.title}}</a>')
    class Meta:
        link = tables.URLColumn()
        model = Job
        fields = ('city', 'title', 'jobtype', 'salary')
