from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Item
from django.template import loader
from django.http import HttpResponse


# Create your views here.
def index(request):
    latest_advert_list = Item.objects.order_by('-modified')[:5]
    context = {
        'latest_advert_list': latest_advert_list,
         }
    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)

    return render(request, 'items/detail.html', {'advert': advert})
