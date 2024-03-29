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
from apps.adverts.views import MapListView
from .filters import ItemsFilter
from .forms import ItemForm
from .models import Item
from .tables import ItemTable
from ..promotions.models import Banner



def index(request):
    query = request.GET.get('q')
    lang = get_language()
    if query:
        advert_list = Item.objects.filter(Q(local__exact=lang) &
                                          (Q(title__icontains=query) | Q(description__icontains=query))
                                          ).order_by('-modified').prefetch_related('author')
    else:
        advert_list = Item.objects.filter(local=lang).order_by('-modified').prefetch_related('author')
    filters = ItemsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)
    favourites = Item.objects.filter(local__exact=lang, favourites__in=[request.user.id]).values_list('id', flat=True)

    header_banners = Banner.objects.filter(local=lang, areas__area='h')
    left_banners = Banner.objects.filter(local=lang, areas__area='l').order_by('?').first()

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'filters': filters,
        'has_filter': has_filter,
        'package_list': 'items:index',  # for filter url
        'favourites': favourites,
        'header_banners': header_banners,
        'left_banners': left_banners

    }
    return render(request, 'items/templates/items/index.html', context)


def detail(request, pk):
    advert = get_object_or_404(Item, pk=pk)
    total_views = 0
    if settings.REDIS:
        r = redis.Redis(connection_pool=settings.POOL)
        redis_key = f'item:{pk}:views'
        if not request.session.get(redis_key):
            request.session[redis_key] = True
            total_views = r.incr(redis_key)
            r.zincrby('ranking:All', 1, f'Item:{advert.id}')
        else:
            total_views = r.get(redis_key).decode('utf-8')

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert,
               'total_views': total_views,
               'favourite': is_favourite,
               'name': 'Item'}
    return render(request, 'items/templates/items/detail.html', context)


class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    login_required = True
    success_url = reverse_lazy('items:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ItemUpdate(UpdateView):
    model = Item
    form_class = ItemForm
    login_required = True
    success_url = reverse_lazy('items:index')


class ItemDelete(DeleteView):
    model = Item
    login_required = True
    success_url = reverse_lazy('items:index')


class ItemTableList(SingleTableMixin, FilterView):
    table_class = ItemTable
    template_name = "items/table.html"
    filterset_class = ItemsFilter

    def get_queryset(self):
        lang = get_language()
        queryset = Item.objects.filter(local__exact=lang)
        return queryset


class ItemMapList(MapListView):
    template_name = 'items/item_map_list.html'
    model = Item
    detail_name_link = "items:detail"
