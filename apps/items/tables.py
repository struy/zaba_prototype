import django_tables2 as tables

from .models import Item


class ItemTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_absolute_url}}">{{record.title}}</a>')

    class Meta:
        link = tables.URLColumn()
        model = Item
        fields = ('city', 'title', 'condition', 'price')
