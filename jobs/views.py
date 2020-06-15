import redis
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .filters import JobsFilter
from .models import Job
from .form import JobForm

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def index(request):
    query = request.GET.get('q')
    if query:
        advert_list = Job.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    else:
        advert_list = Job.objects.order_by('-modified')

    filters = JobsFilter(request.GET, queryset=advert_list)
    page = request.GET.get('page', 1)
    paginator = Paginator(filters.qs, 10)

    try:
        adverts = paginator.page(page)
    except PageNotAnInteger:
        adverts = paginator.page(1)
    except EmptyPage:
        adverts = paginator.page(paginator.num_pages)

    context = {'adverts': adverts,
               'filters': filters
               }
    return render(request, 'jobs/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Job, pk=advert_id)
    total_views = r.incr('job:{}:views'.format(advert.id))
    job_type_dict = {
        'driving': 'car',
        'cleaning': 'broom',
        'construction': 'roller',
        'babysitter': 'baby'
    }
    jobtype = job_type_dict.get(str(advert.jobtype))
    return render(request, 'jobs/detail.html', {'advert': advert, 'total_views': total_views, 'jobtype': jobtype})


class JobList(ListView):
    queryset = Job.objects.filter(point__isnull=False)


class JobCreate(CreateView):
    model = Job
    form_class = JobForm
    login_required = True
    success_url = reverse_lazy('jobs:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class JobUpdate(UpdateView):
    model = Job
    fields = "__all__"
    success_url = reverse_lazy('jobs:index')


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:index')
