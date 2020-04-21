from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index_rents'),
    path('<int:rent_id>/', views.detail, name='detail_rents'),
    path('list', views.rents_list, name='list_rents')

]

