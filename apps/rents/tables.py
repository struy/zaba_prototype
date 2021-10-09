import django_tables2 as tables

from .models import Rental


class RentTable(tables.Table):
    class Meta:
        link = tables.URLColumn()
        model = Rental
        fields = ('city', 'title', 'property_type', 'bathrooms', 'bedrooms', 'price')
