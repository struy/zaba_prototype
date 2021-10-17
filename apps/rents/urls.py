from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'rents'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('map/', views.RentMapList.as_view(), name='map'),
    path('table/', views.RentTableList.as_view(), name='table'),
    path('list', views.rents_list, name='list'),
    path('new', login_required(views.RentCreate.as_view()), name='new'),
    path('edit/<int:pk>', login_required(views.RentUpdate.as_view()), name='edit'),
    path('delete/<int:pk>', login_required(views.RentDelete.as_view()), name='delete'),
]
