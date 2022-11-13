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
from .filters import JobsFilter
from .form import JobForm
from .models import Job
from .tables import JobTable
from ..adverts.views import MapListView

r = redis.Redis(connection_pool=settings.POOL)


def index(request):
    query = request.GET.get('q')
    lang = get_language()
    if query:
        advert_list = Job.objects.filter(Q(local__exact=lang)
                                         & (Q(title__icontains=query) | Q(description__icontains=query))
                                         ).select_related('jobtype').prefetch_related('author').order_by('-modified')
    else:
        advert_list = Job.objects.filter(local=lang).select_related('jobtype').prefetch_related('author').order_by('-modified')

    filters = JobsFilter(request.GET, queryset=advert_list)
    adverts, has_filter = context_helper(request, filters)
    favourites = Job.objects.filter(local__exact=lang, favourites__in=[request.user.id]).values_list('id', flat=True)

    context = {
        'adverts': adverts,
        'is_paginated': True,
        'package_list': 'jobs:index',  # for filter url
        'filters': filters,
        'has_filter': has_filter,
        'favourites': favourites
    }

    return render(request, 'jobs/index.html', context)


def detail(request, pk):
    advert = get_object_or_404(Job, pk=pk)

    if not request.session.get(f'job:{advert.id}:views'):
        request.session[f'job:{advert.id}:views'] = True
        total_views = r.incr(f'job:{advert.id}:views')
        r.zincrby('ranking:All', 1, f'Job:{pk}')
    else:
        total_views = r.get(f'job:{advert.id}:views').decode('utf-8')

    is_favourite = False
    if advert.favourites.filter(id=request.user.id).exists():
        is_favourite = True

    context = {'advert': advert,
               'total_views': total_views,
               'favourite': is_favourite,
               'name': 'Job'}
    return render(request, 'jobs/detail.html', context)


class JobCreate(CreateView):
    model = Job
    form_class = JobForm
    login_required = True
    success_url = reverse_lazy('jobs:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class JobUpdate(UpdateView):
    model = Job
    login_required = True
    form_class = JobForm
    success_url = reverse_lazy('jobs:index')


class JobDelete(DeleteView):
    model = Job
    login_required = True
    success_url = reverse_lazy('jobs:index')


class JobMapList(MapListView):
    template_name = 'jobs/job_map_list.html'
    model = Job
    detail_name_link = "jobs:detail"


class JobTableList(SingleTableMixin, FilterView):
    table_class = JobTable
    template_name = "jobs/table.html"
    filterset_class = JobsFilter

    def get_queryset(self):
        lang = get_language()
        queryset = Job.objects.filter(local__exact=lang)
        return queryset
