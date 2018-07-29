from django.shortcuts import get_object_or_404, render
from .models import Gift



# Create your views here.
def index(request):
    latest_advert_list = Gift.objects.order_by('-updated_at')[:5]
    context = {'latest_advert_list': latest_advert_list}
    return render(request, 'gifts/index.html', context)


def detail(request, advert_id):
    advert = get_object_or_404(Gift, pk=advert_id)
    return render(request, 'gifts/detail.html', {'advert': advert})
