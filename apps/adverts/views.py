import datetime
import redis
import re
from itertools import chain
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.views.generic import ListView
from django.views.decorators.http import require_GET
from django.utils.translation import get_language

from .models import Advert
from apps.items.models import Item
from apps.gifts.models import Gift
from apps.rents.models import Rental
from apps.jobs.models import Job
from apps.services.models import Service
from apps.promotions.models import Promote, Banner
from .utils import get_most_viewed, get_new_ads


def index(request):
    latest_advert_list = Advert.objects.order_by('-updated')[:5]
    template = loader.get_template('adverts/templates/adverts/index.html')
    context = {'latest_advert_list': latest_advert_list, }
    return HttpResponse(template.render(context, request))


def detail(request, advert_id):
    advert = get_object_or_404(Advert, pk=advert_id)
    return render(request, 'adverts/templates/adverts/detail.html', {'advert': advert})


def home(request):
    r = redis.Redis(connection_pool=settings.POOL)
    new = get_new_ads(r)
    most_viewed = get_most_viewed(r)

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
    lang = get_language()
    if lang:
        lang = lang[:2]
    header_banners = Banner.objects.filter(local=lang)

    context = {'total': total,
               'month': month,
               'today': today,
               'week': week,
               'new': new,
               'header_banners': header_banners,
               'most_viewed': most_viewed}

    return render(request, 'home.html', context)


class SearchView(ListView):
    template_name = 'search.html'
    # paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['address'] = self.request.GET.get('address')
        context['has_filter'] = bool(self.request.GET.get('q') or self.request.GET.get('address'))
        # context['is_paginated'] = True
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', "")
        address = request.GET.get('address', "")
        # regular exp for Google API example: Chicago, IL, USA
        if address:
            text = re.search(r'^([\w]*), [A-Z][A-Z], USA', address)
            if text:
                locality = text.group(1)
            else:
                locality = address
        else:
            locality = ""

        if query == "" and locality == "":
            return Item.objects.none()  # just an empty queryset as default

        item_results = None
        job_results = None
        gift_results = None
        rental_results = None
        service_results = None

        if not locality:
            item_results = Item.objects.search(query)
            job_results = Job.objects.search(query)
            gift_results = Gift.objects.search(query)
            rental_results = Rental.objects.search(query)
            service_results = Service.objects.search(query)
        if not query:
            item_results = Item.objects.filter(city__contains=locality)
            job_results = Job.objects.filter(city__contains=locality)
            gift_results = Gift.objects.filter(city__contains=locality)
            rental_results = Rental.objects.filter(city__contains=locality)
            service_results = Service.objects.filter(city__contains=locality)

        if query and locality:
            item_results = Item.objects.search(query).filter(city__contains=locality)
            job_results = Job.objects.search(query).filter(city__contains=locality)
            gift_results = Gift.objects.search(query).filter(city__contains=locality)
            rental_results = Rental.objects.search(query).filter(city__contains=locality)
            service_results = Service.objects.search(query).filter(city__contains=locality)

        # combine querysets
        queryset_chain = chain(
            item_results,
            job_results,
            gift_results,
            rental_results,
            service_results
        )
        qs = sorted(queryset_chain,
                    key=lambda instance: instance.pk,
                    reverse=True)
        self.count = len(qs)  # since qs is actually a list
        return qs


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
