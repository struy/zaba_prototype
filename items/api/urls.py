from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/items/', views.ItemListCreate.as_view()),
]