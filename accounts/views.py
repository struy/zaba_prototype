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
    models = [Item, Job, Rental, Gift]
    ads = [m.objects.filter(favourites=request.user) for m in models]
    adverts = chain(*ads)

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
    ad = get_object_or_404(models[name.capitalize()], id=id)
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
    models = [Item, Job, Rental, Gift]
    adverts = [m.objects.filter(author_id=request.user.id) for m in models]
    ads = [i for i in adverts if len(i)]
    names = [i.model.__name__ + "s" for i in ads]
    all_adverts = dict(zip(names, ads))

    return render(request,
                  'accounts/my_ads.html',
                  {'all_adverts': all_adverts})


def user_ads(request, pk):
    models = [Item, Job, Rental, Gift]
    adverts = [m.objects.filter(author_id=pk) for m in models]
    ads = [i for i in adverts if len(i)]
    names = [i.model.__name__ + "s" for i in ads]
    all_adverts = dict(zip(names, ads))

    return render(request,
                  'accounts/user_ads.html',
                  {'all_adverts': all_adverts})
