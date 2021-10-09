import django_tables2 as tables

from .models import Item


class ItemTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Item
        fields = ('city', 'title', 'condition', 'price')
