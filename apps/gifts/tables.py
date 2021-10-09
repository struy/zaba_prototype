import django_tables2 as tables

from .models import Gift


class GiftTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Gift
        fields = ('city', 'title', 'gift_type')
