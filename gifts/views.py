from django.shortcuts import get_object_or_404, render
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
