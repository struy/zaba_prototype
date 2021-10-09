import redis
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.translation import get_language
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from apps.adverts.utils import context_helper
from .filters import ServicesFilter
from .form import ServiceForm
from .models import Service
# connect to redis
from .tables import ServiceTable
from ..adverts.views import MapListView

r = redis.Redis(connection_pool=settings.POOL)


def index(request):
    query = request.GET.get('q')
    lang = get_language()
    if query:
        advert_list = Service.objects.filter(Q(local__exact=lang)
                                             & (Q(title__icontains=query) | Q(description__icontains=query))
                                             ).prefetch_related('author').order_by('-modified')
    else:
        advert_list = Service.objects.filter(local=lang).prefetch_related('author').order_by('-modified')

    filters = ServicesFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)
    favourites = Service.objects.filter(local__exact=lang, favourites__in=[request.user.id]).values_list('id',
                                                                                                         flat=True)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'package_list': 'Services:index',  # for filter url
        'filters': filters,
        'has_filter': has_filter,
        'favourites': favourites
    }

    return render(request, 'services/templates/services/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Service, pk=advert_id)
    if not request.session.get(f'service:{advert.id}:views'):
        request.session[f'service:{advert.id}:views'] = True
        total_views = r.incr(f'service:{advert.id}:views')
        r.zincrby('ranking:All', 1, f'service:{advert_id}')
    else:
        total_views = r.get(f'service:{advert.id}:views').decode('utf-8')

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert,
               'total_views': total_views,
               'favourite': is_favourite,
               'name': 'Service'
               }
    return render(request, 'services/templates/services/detail.html', context)


class ServiceList(ListView):
    queryset = Service.objects.filter(point__isnull=False)


class ServiceCreate(CreateView):
    model = Service
    form_class = ServiceForm
    login_required = True
    success_url = reverse_lazy('services:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ServiceUpdate(UpdateView):
    model = Service
    login_required = True
    form_class = ServiceForm
    success_url = reverse_lazy('services:index')


class ServiceDelete(DeleteView):
    model = Service
    login_required = True
    success_url = reverse_lazy('services:index')


class ServiceMapList(MapListView):
    template_name = 'services/service_map_list.html'
    model = Service
    detail_name_link = "services:detail"


class ServiceTableList(SingleTableMixin, FilterView):
    table_class = ServiceTable
    template_name = "items/table.html"
    filterset_class = ServicesFilter

    def get_queryset(self):
        lang = get_language()
        queryset = Service.objects.filter(local__exact=lang)
        return queryset
