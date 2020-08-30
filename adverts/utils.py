from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def inform_users(user_id):
    pass


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
