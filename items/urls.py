from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /adverts/5/
    path('<int:advert_id>/', views.detail, name='detail'),

]