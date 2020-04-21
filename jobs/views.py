from django.shortcuts import get_object_or_404, render
from .models import Job
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


def index(request):
    latest_advert_list = Job.objects.order_by('-updated')[:5]
    context = {'latest_advert_list': latest_advert_list}
    return render(request, 'jobs/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Job, pk=advert_id)
    job_type_dict = {
        'driving': 'car',
        'cleaning': 'broom',
        'construction': 'roller',
        'babysitter': 'baby'
    }
    jobtype = job_type_dict.get(str(advert.jobtype))
    return render(request, 'jobs/detail.html', {'advert': advert, 'jobtype': jobtype})


class JobList(ListView):
    model = Job


class JobCreate(CreateView):
    model = Job
    fields = ['title', 'jobtype', 'salary', 'city']
    success_url = reverse_lazy('jobs:job_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class JobUpdate(UpdateView):
    model = Job
    fields = ['title', 'jobtype', 'salary', ]
    success_url = reverse_lazy('jobs:job_list')


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs:job_list')
