import redis
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import generics

from .models import Item
from .forms import ItemForm
from .filters import ItemsFilter
from .serializers import ItemSerializer

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def index(request):
    query = request.GET.get('q')
    if query:
        advert_list = Item.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        advert_list = Item.objects.order_by('-modified')

    filters = ItemsFilter(request.GET, queryset=advert_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(filters.qs, 10)

    try:
        adverts = paginator.page(page)
    except PageNotAnInteger:
        adverts = paginator.page(1)
    except EmptyPage:
        adverts = paginator.page(paginator.num_pages)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'package_list': 'items:index',
        'search': '/result',
        'filters': filters
    }

    return render(request, 'items/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Item, pk=advert_id)
    total_views = r.incr('item:{}:views'.format(advert.id))
    return render(request, 'items/detail.html', {'advert': advert, 'total_views': total_views})


class ItemList(ListView):
    queryset = Item.objects.filter(point__isnull=False)


class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    login_required = True
    success_url = reverse_lazy('items:index')

    # def get_form(self, form_class):
    #     form = super(ItemCreate, self).get_form(form_class)
    #     form.fields['password'].widget = forms.PasswordInput()
    #     return form

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ItemUpdate(UpdateView):
    model = Item
    fields = ['title', 'description', 'image', 'expires', 'price', 'city', 'address', 'point']
    success_url = reverse_lazy('items:index')


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('items:index')


class ItemListCreate(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
