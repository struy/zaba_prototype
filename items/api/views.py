from ..models import Item
from .serializers import ItemSerializer
from rest_framework import generics


class ItemListCreate(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        lang = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
        lang = "en"
        queryset = Item.objects.filter(local__exact=lang)
        return queryset
