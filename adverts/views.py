import redis
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.conf import settings
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
    r = redis.StrictRedis(host=settings.REDIS_HOST,
                          port=settings.REDIS_PORT,
                          db=settings.REDIS_DB)

    total = r.get("Total:saved").decode('utf-8')
    cls = [Item, Gift, Rental, Job]
    month = sum([c.objects.dates('created', 'month').count() for c in cls])
    week = sum([c.objects.dates('created', 'week').count() for c in cls])
    today = sum([c.objects.dates('created', 'day').count() for c in cls])

    context = {'total': total,
               'month': month,
               'today': today,
               'week': week}

    return render(request, 'home.html', context)
