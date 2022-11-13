import django_tables2 as tables

from .models import Rent


class RentTable(tables.Table):
    title = tables.TemplateColumn('<a href="{{ record.get_absolute_url}}">{{record.title}}</a>')

    class Meta:
        link = tables.URLColumn()
        model = Rent
        fields = ('city', 'title', 'property_type', 'bathrooms', 'bedrooms', 'price')
