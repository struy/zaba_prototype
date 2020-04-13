from django.urls import path

from . import views

app_name = 'items'
urlpatterns = [
    path('', views.index, name='index_items'),
    path('<int:advert_id>/', views.detail, name='detail'),
    path('map/', views.ItemList.as_view(), name='map'),
    path('new', views.ItemCreate.as_view(), name='new'),

]
