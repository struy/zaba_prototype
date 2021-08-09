from smtplib import SMTPDataError

from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm


def contact_view(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + ' ' + from_email
            try:
                superusers_emails = [x.email for x in User.objects.filter(is_superuser=True).all()]
                send_mail(subject, message, from_email, superusers_emails)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            except SMTPDataError:
                return redirect('no_success')

            return redirect('success')
    return render(request, "sendemail/templates/sendemail/email.html", {'form': form})


def success_view(request):
    return render(request, "sendemail/templates/sendemail/success.html", {'success': True})


def no_success_view(request):
    return render(request, "sendemail/templates/sendemail/no_success.html", {'success': False})
