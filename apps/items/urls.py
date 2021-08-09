from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:advert_id>/', views.detail, name='detail'),
    path('map/', views.ItemList.as_view(), name='map'),
    path('table/', views.ItemTableList.as_view(), name='table'),
    path('new', login_required(views.ItemCreate.as_view()), name='new'),
    path('edit/<int:pk>', login_required(views.ItemUpdate.as_view()), name='edit'),
    path('delete/<int:pk>', login_required(views.ItemDelete.as_view()), name='delete'),

]
