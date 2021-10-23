import datetime
import re
from itertools import chain

import redis
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.utils.translation import get_language
from django.views.decorators.http import require_GET
from django.views.generic import ListView
from pytz import utc

from apps.gifts.models import Gift
from apps.items.models import Item
from apps.jobs.models import Job
from apps.promotions.models import Banner
from apps.rents.models import Rent
from apps.services.models import Service
from .models import Advert
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

    counter = {
        'total': total,
        'month': month,
        'week': week,
        'today': today
    }

    lang = get_language()
    if lang:
        lang = lang[:2]
    sm_header_banners = Banner.objects.filter(local=lang, areas__area='h', size='sm').order_by('?')
    md_header_banners = Banner.objects.filter(local=lang, areas__area='h', size='md').order_by('?')
    lg_header_banners = Banner.objects.filter(local=lang, areas__area='h', size='lg').order_by('?')
    bottom_banners = Banner.objects.filter(local=lang, areas__area='b').order_by('?').first()

    context = {'counter': counter,
               'new': new,
               'sm_header_banners': sm_header_banners,
               'md_header_banners': md_header_banners,
               'lg_header_banners': lg_header_banners,
               'bottom_banners': bottom_banners,
               'most_viewed': most_viewed}

    return render(request, 'home.html', context)


class SearchView(ListView):
    template_name = 'search.html'
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['address'] = self.request.GET.get('address')
        context['has_filter'] = bool(self.request.GET.get('q') or self.request.GET.get('address'))
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
            rental_results = Rent.objects.search(query)
            service_results = Service.objects.search(query)
        if not query:
            item_results = Item.objects.filter(city__contains=locality)
            job_results = Job.objects.filter(city__contains=locality)
            gift_results = Gift.objects.filter(city__contains=locality)
            rental_results = Rent.objects.filter(city__contains=locality)
            service_results = Service.objects.filter(city__contains=locality)

        if query and locality:
            item_results = Item.objects.search(query).filter(city__contains=locality)
            job_results = Job.objects.search(query).filter(city__contains=locality)
            gift_results = Gift.objects.search(query).filter(city__contains=locality)
            rental_results = Rent.objects.search(query).filter(city__contains=locality)
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


class MapList(ListView):
    context_object_name = 'adverts'
    template_name = 'adverts/map.html'

    def get_queryset(self):
        lang = get_language()
        queryset = {'items': Item.objects.filter(point__isnull=False, local__exact=lang),
                    'jobs': Job.objects.filter(point__isnull=False, local__exact=lang),
                    'gifts': Gift.objects.filter(point__isnull=False, local__exact=lang),
                    'rents': Rent.objects.filter(point__isnull=False, local__exact=lang)
                    }
        return queryset


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /private/",
        "Disallow: /junk/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


class MapListView(ListView):
    context_object_name = 'adverts'
    detail_name_link = ""
    template_name = ''
    # example for Item
    model = Item

    def get_queryset(self):
        lang = get_language()
        now = utc.localize(datetime.datetime.today())
        new = now - datetime.timedelta(weeks=2)
        old = now - datetime.timedelta(weeks=4)
        very_old = now - datetime.timedelta(weeks=12)
        dead = now - datetime.timedelta(weeks=24)
        queryset = {'new_items': self.model.objects.filter(point__isnull=False, local__exact=lang, modified__gte=new),
                    'not_new_items': self.model.objects.filter(point__isnull=False, local__exact=lang,
                                                               modified__range=[very_old, new]),
                    # 'other_items': self.model.objects.filter(point__isnull=False, local__exact=lang,
                    #                                          modified__range=[old, new]),
                    #
                    # 'old_items': self.model.objects.filter(point__isnull=False, local__exact=lang,
                    #                                        modified__range=[very_old, old]),
                    # 'very_old_items': self.model.objects.filter(point__isnull=False, local__exact=lang,
                    #                                             modified__range=[dead, very_old]),
                    # 'dead_items': self.model.objects.filter(point__isnull=False, local__exact=lang, modified__lt=dead),
                    }
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['detail_name_link'] = self.detail_name_link
        return context
