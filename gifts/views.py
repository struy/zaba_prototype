import redis
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.conf import settings

from adverts.utils import context_helper
from .form import GiftForm
from .filters import GiftsFilter
from .models import Gift

# connect to redis
r = redis.Redis(connection_pool=settings.POOL)


def index(request):
    query = request.GET.get('q')
    lang = request.LANGUAGE_CODE
    if query:
        advert_list = Gift.objects.filter(Q(local__exact=lang) &
                                          (Q(title__icontains=query) | Q(description__icontains=query))
                                          ).order_by('-modified')
    else:
        advert_list = Gift.objects.filter(local=lang).order_by('-modified')
    filters = GiftsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)

    context = {'adverts': adverts,
               'filters': filters,
               'has_filter': has_filter,
               'package_list': 'gifts:index',
               }
    return render(request, 'gifts/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Gift, pk=advert_id)
    total_views = r.incr('gift:{}:views'.format(advert.id))
    return render(request, 'gifts/detail.html', {'advert': advert,
                                                 'total_views': total_views})


class GiftList(ListView):
    queryset = Gift.objects.filter(point__isnull=False)


class GiftCreate(CreateView):
    model = Gift
    form_class = GiftForm
    login_required = True
    success_url = reverse_lazy('gifts:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class GiftUpdate(UpdateView):
    model = Gift
    form_class = GiftForm
    login_required = True
    success_url = reverse_lazy('gifts:index')


class GiftDelete(DeleteView):
    model = Gift
    login_required = True
    success_url = reverse_lazy('gifts:index')
