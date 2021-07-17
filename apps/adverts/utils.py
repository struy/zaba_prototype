from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.items.models import Item
from apps.gifts.models import Gift
from apps.rents.models import Rental
from apps.jobs.models import Job


def inform_users(user_id):
    """send notification for user"""
    pass


def get_most_viewed(pool):
    result = []
    ranking = [i.decode('utf-8') for i in pool.zrange('ranking:All', 0, -1, desc=True)[:12]]
    models = {"Item": Item, "Job": Job, "Gift": Gift, "Rental": Rental}

    for key, value in models.items():
        ranking_ids = [int(item[len(key) + 1:]) for item in ranking if item.startswith(key)]
        viewed = list(value.objects.filter(
            id__in=ranking_ids))
        viewed.sort(key=lambda x: ranking_ids.index(x.id))
        result.append(viewed)

    most_viewed = chain(*result)
    return most_viewed


def get_new_ads(pool):
    models = ["Item", "Job", "Gift", "Rental"]
    result = []
    for name in models:
        ids = [int(i) for i in pool.lrange(f'{name}:new', 0, 12)]
        result.append(list(Item.objects.filter(id__in=ids)))
    new = chain(*result)
    return new


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
