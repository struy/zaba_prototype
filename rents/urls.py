from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /rents/5/
    path('<int:rent_id>/', views.detail, name='detail'),
    path('list', views.rents_list, name='list')

]
