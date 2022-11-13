from itertools import chain
from smtplib import SMTPDataError

import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.gifts.models import Gift
from apps.items.models import Item
from apps.jobs.models import Job
from apps.rents.models import Rent
from apps.services.models import Service
from .forms import UserEditForm, ContactUserForm
from .forms import UserRegistrationForm


@login_required
def favourite_list(request):
    models = [Item, Job, Rent, Gift]
    ads = [m.objects.filter(favourites=request.user) for m in models]
    adverts = chain(*ads)

    return render(request,
                  'accounts/templates/accounts/favourites.html',
                  {'adverts': adverts})


class AdFavAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, name=None, record_id=None):
        models = {
            "Item": Item,
            "Job": Job,
            "Gift": Gift,
            "Rent": Rent,
            "Service": Service
        }
        ad = get_object_or_404(models[name.capitalize()], id=record_id)
        user = self.request.user
        updated = False
        favourite = False
        if ad:  # and user.is_authenticated()
            r = redis.Redis(connection_pool=settings.POOL)
            if ad.favourites.filter(id=user.id).exists():
                ad.favourites.remove(user)
                r.decr(f'Author:fav:{user.id}')
                favourite = False
            else:
                ad.favourites.add(user)
                r.incr(f'Author:fav:{user.id}')
                favourite = True
            updated = True

        data = {
            "updated": updated,
            "favourite": favourite
        }
        return Response(data)


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
            return render(request, 'accounts/templates/accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/templates/accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/templates/accounts/edit.html', {'user_form': user_form})


@login_required
def my_ads(request):
    models = [Item, Job, Rent, Gift]
    adverts = [m.objects.filter(author_id=request.user.id) for m in models]
    ads = [i for i in adverts if len(i)]
    names = [i.model.__name__ + "s" for i in ads]
    # fix for rents view
    if "rentals" in names:
        names[names.index("rentals")] = "rents"
    all_adverts = dict(zip(names, ads))

    return render(request,
                  'accounts/templates/accounts/my_ads.html',
                  {'all_adverts': all_adverts})


def user_ads(request, pk):
    models = [Item, Job, Rent, Gift, Service]
    adverts = [m.objects.filter(author_id=pk) for m in models]
    ads = [i for i in adverts if len(i)]
    names = [i.model.__name__ + "s" for i in ads]
    # fix for rents view
    if "rentals" in names:
        names[names.index("rentals")] = "rents"
    all_adverts = dict(zip(names, ads))

    return render(request,
                  'accounts/templates/accounts/user_ads.html',
                  {'all_adverts': all_adverts})


def contact_user(request, pk, name, a_id):
    user = get_object_or_404(User, pk=pk)
    models = {
        "Item": Item,
        "Job": Job,
        "Gift": Gift,
        "Rent": Rent
    }
    advert = get_object_or_404(models[name.capitalize()], id=a_id)
    if request.method == 'GET':
        form = ContactUserForm()
    else:
        form = ContactUserForm(request.POST)
        if form.is_valid():
            subject = advert.title
            to_email = [user.email]
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + ' ' + from_email
            try:
                send_mail(subject, message, from_email, to_email)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except SMTPDataError:
                return redirect('no_success')

            return redirect('success')
    return render(request, "accounts/templates/accounts/connect.html", {'form': form})


User = get_user_model()


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'accounts/user_confirm_delete.html'
