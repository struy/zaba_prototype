import redis
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.db.models import Q

from adverts.utils import context_helper
from .models import Rental, RentalTable
from .forms import RentForm
from .filters import RentsFilter

# connect to redis
r = redis.Redis(connection_pool=settings.POOL)


def index(request):
    query = request.GET.get('q')
    lang = request.LANGUAGE_CODE
    if query:
        advert_list = Rental.objects.filter(Q(local__exact=lang) &
                                            (Q(title__icontains=query) | Q(description__icontains=query))
                                            ).order_by('-modified')
    else:
        advert_list = Rental.objects.filter(local=lang).order_by('-modified')

    filters = RentsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'package_list': 'rents:index',
        'filters': filters,
        'has_filter': has_filter,
    }

    return render(request, 'rents/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Rental, pk=advert_id)
    total_views = r.incr('rent:{}:views'.format(advert.id))
    return render(request, 'rents/detail.html', {'advert': advert, 'total_views': total_views})


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
