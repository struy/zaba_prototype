from django.shortcuts import get_object_or_404, render
from .models import Job
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.
def index(request):
    latest_advert_list = Job.objects.order_by('-updated_at')[:5]
    context = {'latest_advert_list': latest_advert_list}
    return render(request, 'jobs/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Job, pk=advert_id)
    job_type_dict = {
        'Driving': 'car',
        'Cleaning': 'broom',
        'Construction': 'roller'
    }
    jobtype = job_type_dict[str(advert.jobtype)]
    return render(request, 'jobs/detail.html', {'advert': advert, 'jobtype': jobtype})


class JobList(ListView):
    model = Job


class JobCreate(CreateView):
    model = Job
    fields = ['title', 'jobtype', 'salary', 'location']
    success_url = reverse_lazy('jobs_cbv:job_list')

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)


# Note
# that
# you’ll
# need
# to
# decorate
# this
# view
# using
# login_required(), or alternatively
# handle
# unauthorized
# users in the
# form_valid().


class JobUpdate(UpdateView):
    model = Job
    fields = ['title', 'jobtype', 'salary', 'location']
    success_url = reverse_lazy('jobs_cbv:job_list')


class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy('jobs_cbv:job_list')
