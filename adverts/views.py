import datetime
import redis
from itertools import chain
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render, reverse
from django.conf import settings
from django.views.generic import ListView

from .models import Advert
from items.models import Item
from gifts.models import Gift
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

    total = r.get("Total:saved")

    if total:
        total = total.decode('utf-8')

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


class SearchView(ListView):
    template_name = 'search.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        locality = request.GET.get('address', None)

        if query:
            if locality:
                item_results = Item.objects.search(query)
                job_results = Job.objects.search(query)
                gift_results = Gift.objects.search(query)
                rental_results = Rental.objects.search(query)
            else:
                item_results = Item.objects.search(query).filter(city__contains=locality)
                job_results = Job.objects.search(query).filter(city__contains=locality)
                gift_results = Gift.objects.search(query).filter(city__contains=locality)
                rental_results = Rental.objects.search(query).filter(city__contains=locality)

            # combine querysets
            queryset_chain = chain(
                item_results,
                job_results,
                gift_results,
                rental_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Item.objects.none()  # just an empty queryset as default


