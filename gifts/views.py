from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .form import GiftForm
from .models import Gift
import redis
from django.conf import settings

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


def index(request):
    latest_advert_list = Gift.objects.order_by('-modified')[:5]
    context = {'latest_advert_list': latest_advert_list}
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
        form.instance.owner = self.request.user
        return super().form_valid(form)


class GiftUpdate(UpdateView):
    model = Gift
    fields = '__all__'
    success_url = reverse_lazy('gifts:index')


class GiftDelete(DeleteView):
    model = Gift
    success_url = reverse_lazy('gifts:index')
