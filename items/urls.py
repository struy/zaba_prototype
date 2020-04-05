from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index_items'),
    path('<int:advert_id>/', views.detail, name='detail_items'),
]
