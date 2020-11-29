from django.apps import AppConfig
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

    new = items + jobs + rents + gifts

    return render(request,
                  'accounts/favourites.html',
                  {'new': new})


@login_required
def favourite_add(request, name, d):
    model = AppConfig.get_models(name)
    ad = get_object_or_404(model, id=d)
    if ad.favourites.filter(id=request.user.id).exists():
        ad.favourites.remove(request.user)
    else:
        ad.favourites.add(request.user)
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
