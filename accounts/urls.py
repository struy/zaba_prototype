from django.urls import path, include
from .views import register, edit, my_ads, favourite_add, favourite_list
from django.contrib.auth import views as auth_views

# app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('edit/', edit, name='profile_edit'),
    path('fav/<str:name>/<int:id>', favourite_add, name='favourite_add'),
    path('favorites/', favourite_list, name="favorites"),
    path('my_ads/', my_ads, name='my_ads'),
    # change password urls
    path('password_change/', auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(),
         name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    # for fix example.com in reset email go to  /admin/sites/site/1/change/
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
