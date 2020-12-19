from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from items.models import Item
from gifts.models import Gift
from rents.models import Rental
from jobs.models import Job


def inform_users(user_id):
    """send notification for user"""
    pass


def get_most_viewed(pool):
    # get all
    ranking = pool.zrange('ranking:All', 0, -1, desc=True)[:12]
    # get Items
    item_ranking_ids = [int(item[5:]) for item in ranking if item.decode('utf-8').startswith("Item")]
    most_viewed_item = list(Item.objects.filter(
        id__in=item_ranking_ids))
    most_viewed_item.sort(key=lambda x: item_ranking_ids.index(x.id))
    # get Jobs
    job_ranking_ids = [int(job[4:]) for job in ranking if job.decode('utf-8').startswith("Job")]
    most_viewed_job = list(Job.objects.filter(
        id__in=job_ranking_ids))
    most_viewed_job.sort(key=lambda x: job_ranking_ids.index(x.id))
    # get Rents
    rent_ranking_ids = [int(rent[7:]) for rent in ranking if rent.decode('utf-8').startswith("Rental")]
    most_viewed_rent = list(Rental.objects.filter(
        id__in=rent_ranking_ids))
    most_viewed_rent.sort(key=lambda x: rent_ranking_ids.index(x.id))
    # get Gifts
    gift_ranking_ids = [int(gift[7:]) for gift in ranking if gift.decode('utf-8').startswith("Gift")]
    most_viewed_gift = list(Gift.objects.filter(
        id__in=gift_ranking_ids))
    most_viewed_gift.sort(key=lambda x: gift_ranking_ids.index(x.id))

    most_viewed = chain(most_viewed_job,
                        most_viewed_item,
                        rent_ranking_ids,
                        gift_ranking_ids
                        )
    return most_viewed


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
