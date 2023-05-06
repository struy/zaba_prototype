import redis
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import get_language
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.adverts.utils import context_helper
from .filters import RentsFilter
from .forms import RentForm
from .models import Rent, RentalTable
from .tables import RentTable
from ..adverts.views import MapListView



def index(request):
    query = request.GET.get('q')
    lang = get_language()
    if query:
        advert_list = Rent.objects.filter(Q(local__exact=lang) &
                                          (Q(title__icontains=query) | Q(description__icontains=query))
                                          ).select_related('property_type').prefetch_related('author').order_by('-modified')
    else:
        advert_list = Rent.objects.filter(local=lang).select_related('property_type').prefetch_related('author').order_by('-modified')

    filters = RentsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)
    favourites = Rent.objects.filter(local__exact=lang, favourites__in=[request.user.id]).values_list('id', flat=True)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'filters': filters,
        'has_filter': has_filter,
        'package_list': 'rents:index',  # for filter url
        'favourites': favourites
    }

    return render(request, 'rents/templates/rents/index.html', context)


def detail(request, pk):
    advert = get_object_or_404(Rent, pk=pk)
    if settings.REDIS:
        r = redis.Redis(connection_pool=settings.POOL)
        if not request.session.get(f'rent:{advert.id}:views'):
            request.session[f'rent:{advert.id}:views'] = True
            total_views = r.incr(f'rent:{advert.id}:views')
            r.zincrby('ranking:All', 1, f'Rent:{pk}')
        else:
            total_views = r.get(f'rent:{advert.id}:views').decode('utf-8')
    else:
        total_views = 0

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert,
               'total_views': total_views,
               'favourite': is_favourite,
               'name': 'Rent'}
               
    return render(request, 'rents/templates/rents/detail.html', context)


def rents_list(request):
    queryset = Rent.objects.all()
    table = RentalTable(queryset)
    return render(request, 'rents/templates/rents/rent_table_list.html', {'table': table})


class RentCreate(CreateView):
    model = Rent
    form_class = RentForm
    login_required = True
    success_url = reverse_lazy('rents:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RentUpdate(UpdateView):
    model = Rent
    form_class = RentForm
    login_required = True
    success_url = reverse_lazy('rents:index')


class RentDelete(DeleteView):
    model = Rent
    login_required = True
    success_url = reverse_lazy('rents:index')


class RentMapList(MapListView):
    template_name = 'rents/rent_map_list.html'
    model = Rent
    detail_name_link = "rents:detail"


class RentTableList(SingleTableMixin, FilterView):
    table_class = RentTable
    template_name = "rents/table.html"
    filterset_class = RentsFilter

    def get_queryset(self):
        lang = get_language()
        queryset = Rent.objects.filter(local__exact=lang)
        return queryset
