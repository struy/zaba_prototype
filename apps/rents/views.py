import redis
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import get_language
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from apps.adverts.utils import context_helper
from .filters import RentsFilter
from .forms import RentForm
from .models import Rental, RentalTable
# connect to redis
from ..adverts.views import MapListView

r = redis.Redis(connection_pool=settings.POOL)


def index(request):
    query = request.GET.get('q')
    lang = get_language()
    if query:
        advert_list = Rental.objects.filter(Q(local__exact=lang) &
                                            (Q(title__icontains=query) | Q(description__icontains=query))
                                            ).prefetch_related('author').order_by('-modified')
    else:
        advert_list = Rental.objects.filter(local=lang).prefetch_related('author').order_by('-modified')

    filters = RentsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)
    favourites = Rental.objects.filter(local__exact=lang, favourites__in=[request.user.id]).values_list('id', flat=True)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'filters': filters,
        'has_filter': has_filter,
        'package_list': 'rents:index',  # for filter url
        'favourites': favourites
    }

    return render(request, 'rents/templates/rents/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Rental, pk=advert_id)

    if not request.session.get(f'rent:{advert.id}:views'):
        request.session[f'rent:{advert.id}:views'] = True
        total_views = r.incr(f'rent:{advert.id}:views')
        r.zincrby('ranking:All', 1, f'Rental:{advert_id}')
    else:
        total_views = r.get(f'rent:{advert.id}:views').decode('utf-8')

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert,
               'total_views': total_views,
               'favourite': is_favourite,
               'name': 'Rental'}
    return render(request, 'rents/templates/rents/detail.html', context)


def rents_list(request):
    queryset = Rental.objects.all()
    table = RentalTable(queryset)
    return render(request, 'rents/templates/rents/rental_table_list.html', {'table': table})


class RentCreate(CreateView):
    model = Rental
    form_class = RentForm
    login_required = True
    success_url = reverse_lazy('rents:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RentUpdate(UpdateView):
    model = Rental
    form_class = RentForm
    login_required = True
    success_url = reverse_lazy('rents:index')


class RentDelete(DeleteView):
    model = Rental
    login_required = True
    success_url = reverse_lazy('rents:index')


class RentMapList(MapListView):
    template_name = 'rents/rent_map_list.html'
    model = Rental
    detail_name_link = "rents:detail"
