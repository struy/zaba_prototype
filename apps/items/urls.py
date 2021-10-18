from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('map/', views.ItemMapList.as_view(), name='map'),
    path('table/', views.ItemTableList.as_view(), name='table'),
    path('new/', login_required(views.ItemCreate.as_view()), name='new'),
    path('edit/<int:pk>/', login_required(views.ItemUpdate.as_view()), name='edit'),
    path('delete/<int:pk>/', login_required(views.ItemDelete.as_view()), name='delete'),

]
