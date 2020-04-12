from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Advert
from gifts.models import Gift
from items.models import Item
from rents.models import Rental
from jobs.models import Job


def index(request):
    latest_advert_list = Advert.objects.order_by('-updated')[:5]
    template = loader.get_template('adverts/index.html')
    context = {'latest_advert_list': latest_advert_list, }
    return HttpResponse(template.render(context, request))


def detail(request, advert_id):
    advert = get_object_or_404(Advert, pk=advert_id)
    return render(request, 'adverts/detail.html', {'advert': advert})


def home(request):
    total = Gift.objects.count() + Item.objects.count() + Rental.objects.count() + Job.objects.count()
    month = Item.objects.dates('created', 'month').count()
    week = Item.objects.dates('created', 'week').count()
    today = Item.objects.dates('created', 'day').count()

    context = {'total': total,
               'month': month,
               'today': today,
               'week': week}

    return render(request, 'home.html', context)
