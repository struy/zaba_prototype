from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Item


def index(request):
    latest_advert_list = Item.objects.order_by('-modified')[:5]
    context = {
        'latest_advert_list': latest_advert_list,
    }
    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)
    return render(request, 'items/detail.html', {'advert': advert})


class ItemList(ListView):
    queryset = Item.objects.filter(point__isnull=False)

