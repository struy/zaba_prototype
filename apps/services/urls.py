from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'services'
urlpatterns = [
    path('', views.index, name='index'),
    path('map', views.ServiceList.as_view(), name='map'),
    path('<int:advert_id>/', views.detail, name='detail'),
    path('new', login_required(views.ServiceCreate.as_view()), name='new'),
    path('edit/<int:pk>', login_required(views.ServiceUpdate.as_view()), name='edit'),
    path('delete/<int:pk>', login_required(views.ServiceDelete.as_view()), name='delete'),
]
