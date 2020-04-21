from django.urls import path
from . import views

app_name = 'gifts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:advert_id>/', views.detail, name='detail'),
    path('map/', views.GiftList.as_view(), name='map'),
    path('new', views.GiftCreate.as_view(), name='new'),
    path('edit/<int:pk>', views.GiftUpdate.as_view(), name='edit'),
    path('delete/<int:pk>', views.GiftDelete.as_view(), name='delete'),
]
