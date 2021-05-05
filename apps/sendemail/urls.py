from django.urls import path

from .views import contact_view, success_view, no_success_view

urlpatterns = [
    path('contact/', contact_view, name='contact'),
    path('success/', success_view, name='success'),
    path('no_success/', no_success_view, name='no_success'),
]