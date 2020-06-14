import redis
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .models import Rental, RentalTable
from .forms import RentForm
from .filters import RentsFilter

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def index(request):
    query = request.GET.get('q')
    if query:
        advert_list = Rental.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        advert_list = Rental.objects.order_by('-modified')

    filters = RentsFilter(request.GET, queryset=advert_list)
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
        'package_list': 'rents:index',
        'filters': filters
    }

    return render(request, 'rents/index.html', context)


def detail(request, rent_id):
    rent = get_object_or_404(Rental, pk=rent_id)
    return render(request, 'rents/detail.html', {'rent': rent})


def rents_list(request):
    queryset = Rental.objects.all()
    table = RentalTable(queryset)
    return render(request, 'rents/rental_table_list.html', {'table': table})


class RentList(ListView):
    queryset = Rental.objects.filter(point__isnull=False)


class RentCreate(CreateView):
    model = Rental
    form_class = RentForm
    login_required = True
    success_url = reverse_lazy('rents:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RentUpdate(UpdateView):
    model = Rental
    fields = ['title', 'description', 'image', 'expires', 'price', 'city', 'address', 'point']
    success_url = reverse_lazy('items:index')


class RentDelete(DeleteView):
    model = Rental
    success_url = reverse_lazy('items:index')



