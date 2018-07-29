from django.shortcuts import render, get_object_or_404
from .models import Rental, RentalTable
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    latest_rent_list = Rental.objects.order_by('-created_at')[:5]
    template = loader.get_template('rents/index.html')
    context = {
        'latest_rent_list': latest_rent_list,
           }
    return HttpResponse(template.render(context, request))


def detail(request, rent_id):
    rent = get_object_or_404(Rental, pk=rent_id)
    return render(request, 'rents/detail.html', {'rent': rent})



def rents_list(request):
    queryset = Rental.objects.all()
    table = RentalTable(queryset)
    return render(request, 'rents/rental_list.html', {'table': table})