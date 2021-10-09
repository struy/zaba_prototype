from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.JobMapList.as_view(), name='map'),
    path('table/', views.JobTableList.as_view(), name='table'),
    path('<int:advert_id>/', views.detail, name='detail'),
    path('new', login_required(views.JobCreate.as_view()), name='new'),
    path('edit/<int:pk>', login_required(views.JobUpdate.as_view()), name='edit'),
    path('delete/<int:pk>', login_required(views.JobDelete.as_view()), name='delete'),
]
