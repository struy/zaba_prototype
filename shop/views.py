from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product


@login_required
def checkout(request):
    products = Product.objects.all()
    return render(request, 'shop/product/checkout.html', {'products': products})
