from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.MapList.as_view(), name='home_map'),
]
