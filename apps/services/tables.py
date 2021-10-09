import django_tables2 as tables

from .models import Service


class ServiceTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Service
        fields = ('city', 'title', 'salary')
