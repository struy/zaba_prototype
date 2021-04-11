import redis
from django.shortcuts import get_object_or_404, render
from django.utils.translation import get_language
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.db.models import Q

from adverts.utils import context_helper
from .models import Item
from .forms import ItemForm
from .filters import ItemsFilter

# connect to redis
r = redis.Redis(connection_pool=settings.POOL)


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
    context = {
        'adverts': adverts,
        'is_paginated': True,
        'filters': filters,
        'has_filter': has_filter,
        'package_list': 'items:index',  # for filter url
        'favourites': favourites
    }

    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)

    if not request.session.get(f'item:{advert.id}:views'):
        request.session[f'item:{advert.id}:views'] = True
        total_views = r.incr(f'item:{advert.id}:views')
        r.zincrby('ranking:All', 1, f'Item:{advert_id}')
    else:
        total_views = r.get(f'item:{advert.id}:views').decode('utf-8')

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert, 'total_views': total_views, 'favourite': is_favourite}
    return render(request, 'items/detail.html', context)


class ItemList(ListView):
    queryset = Item.objects.filter(point__isnull=False)


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
