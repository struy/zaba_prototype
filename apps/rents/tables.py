import django_tables2 as tables

from .models import Rent


class RentTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Rent
        fields = ('city', 'title', 'property_type', 'bathrooms', 'bedrooms', 'price')
