import datetime
import redis
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from .models import Advert


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

    # cls = [Item, Gift, Rental, Job]
    # month = sum([c.objects.dates('created', 'month').count() for c in cls])

    now = datetime.datetime.now()
    month_ago = now - datetime.timedelta(weeks=4)
    week_ago = now - datetime.timedelta(weeks=1)
    day_ago = now - datetime.timedelta(days=1)

    month = r.zcount("adverts", month_ago.timestamp(), "+inf")
    week = r.zcount("adverts", week_ago.timestamp(), "+inf")
    today = r.zcount("adverts", day_ago.timestamp(), "+inf")

    context = {'total': total,
               'month': month,
               'today': today,
               'week': week}

    return render(request, 'home.html', context)
