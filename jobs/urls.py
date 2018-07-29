from django.urls import path

from . import views

app_name = 'jobs_cbv'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.JobList.as_view(), name='job_list'),
    # ex: /adverts/5/
    path('<int:advert_id>/', views.detail, name='detail'),
    path('new', views.JobCreate.as_view(), name='job_new'),
    path('edit/<int:pk>', views.JobUpdate.as_view(), name='job_edit'),
    path('delete/<int:pk>', views.JobDelete.as_view(), name='job_delete'),

]