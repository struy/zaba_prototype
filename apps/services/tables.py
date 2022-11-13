import django_tables2 as tables

from .models import Service


class ServiceTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_absolute_url}}">{{record.title}}</a>')
    class Meta:
        link = tables.URLColumn()
        model = Service
        fields = ('city', 'title', 'salary')
