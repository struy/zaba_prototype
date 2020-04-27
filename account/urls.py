from django.urls import path, include
from .views import register as view_register


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', view_register, name='register'),
]
