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
        advert_list = Item.objects.filter(Q(local__exact=lang)
                                          & (Q(title__icontains=query) | Q(description__icontains=query))
                                          ).order_by('-modified')
    else:
        advert_list = Item.objects.filter(local=lang).order_by('-modified')

    filters = ItemsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'package_list': 'items:index',
        'filters': filters,
        'has_filter': has_filter
    }

    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)
    total_views = r.incr('item:{}:views'.format(advert.id))
    # increment image ranking by 1
    r.zincrby('ranking:Item', int(advert_id), 1)
    return render(request, 'items/detail.html', {'advert': advert, 'total_views': total_views})


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
