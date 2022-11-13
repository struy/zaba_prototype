import django_tables2 as tables

from .models import Gift


class GiftTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_absolute_url}}">{{record.title}}</a>')

    class Meta:
        link = tables.URLColumn()
        model = Gift
        fields = ('city', 'title', 'gift_type')
