from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'gifts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('map/', views.GiftMapList.as_view(), name='map'),
    path('table/', views.GiftTableList.as_view(), name='table'),
    path('new/', login_required(views.GiftCreate.as_view()), name='new'),
    path('edit/<int:pk>/', login_required(views.GiftUpdate.as_view()), name='edit'),
    path('delete/<int:pk>/', login_required(views.GiftDelete.as_view()), name='delete'),
]
