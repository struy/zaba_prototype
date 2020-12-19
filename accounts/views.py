from itertools import chain
import redis

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from gifts.models import Gift
from items.models import Item
from jobs.models import Job
from rents.models import Rental
from .forms import UserEditForm
from .forms import UserRegistrationForm


@login_required
def favourite_list(request):
    items = Item.objects.filter(favourites=request.user)
    jobs = Job.objects.filter(favourites=request.user)
    rents = Rental.objects.filter(favourites=request.user)
    gifts = Gift.objects.filter(favourites=request.user)
    adverts = chain(items,
                    jobs,
                    rents,
                    gifts)

    return render(request,
                  'accounts/favourites.html',
                  {'adverts': adverts})


@login_required
def favourite_add(request, name, id):
    models = {
        "Item": Item,
        "Job": Job,
        "Gift": Gift,
        "Rental": Rental
    }
    # AppConfig.get_models(name)
    ad = get_object_or_404(models[name], id=id)
    if ad:
        r = redis.Redis(connection_pool=settings.POOL)

        if ad.favourites.filter(id=request.user.id).exists():
            ad.favourites.remove(request.user)
            r.decr(f'Author:fav:{request.user.id}')
        else:
            ad.favourites.add(request.user)
            r.incr(f'Author:fav:{request.user.id}')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/edit.html', {'user_form': user_form})


@login_required
def my_ads(request):
    items = Item.objects.filter(author=request.user)
    jobs = Job.objects.filter(author=request.user)
    rents = Rental.objects.filter(author=request.user)
    gifts = Gift.objects.filter(author=request.user)
    adverts = chain(items,
                    jobs,
                    rents,
                    gifts)

    return render(request,
                  'accounts/my_ads.html',
                  {'adverts': adverts})
