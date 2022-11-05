from random import shuffle
from itertools import chain

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.items.models import Item
from apps.gifts.models import Gift
from apps.rents.models import Rent
from apps.jobs.models import Job
from apps.services.models import Service


def inform_users(user_id):
    """send notification for user"""
    pass


def get_most_viewed(pool):
    ads = cache.get('most_viewed')
    if ads is None:
        ads = query_most_viewed(pool)
        cache.set('most_viewed', ads, 900)
    return ads


def query_most_viewed(pool):
    result = []
    ranking = [i.decode('utf-8') for i in pool.zrange('ranking:All', 0, -1, desc=True)[:12]]
    models = {"Item": Item, "Job": Job, "Gift": Gift, "Rent": Rent, "Service": Service}
    for key, value in models.items():
        ranking_ids = [int(item[len(key) + 1:]) for item in ranking if item.startswith(key)]
        viewed = list(value.objects.filter(
            id__in=ranking_ids))
        viewed.sort(key=lambda x: ranking_ids.index(x.id))
        result.append(viewed)
    most_viewed = chain(*result)
    return most_viewed


def get_new_ads(pool):
    ads = cache.get('new_ads')
    if ads is None:
        ads = query_new_ads(pool)
        cache.set('new_ads', ads, 900)
    return ads


def query_new_ads(pool):
    models = {"Item": Item, "Job": Job, "Gift": Gift, "Rent": Rent, "Service": Service}
    result = []
    for name, model in models.items():
        ids = [int(i) for i in pool.lrange(f'{name}:new', 0, 4)]
        result.append(list(model.objects.filter(id__in=ids)))
    shuffle(result)
    return chain(*result)


def context_helper(request, filters):
    """check filter and make pagination for context"""
    has_filter = any(field in request.GET for field in set(filters.get_fields()))
    page = request.GET.get('page', 1)
    paginator = Paginator(filters.qs, 10)

    try:
        adverts = paginator.page(page)
    except PageNotAnInteger:
        adverts = paginator.page(1)
    except EmptyPage:
        adverts = paginator.page(paginator.num_pages)

    return adverts, has_filter
