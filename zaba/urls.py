from django.contrib import admin
from django.urls import path, include
from adverts import views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('search', views.SearchView.as_view(), name="global_search"),
    path('jobs/', include('jobs.urls')),
    path('rents/', include('rents.urls')),
    path('items/', include('items.urls')),
    path('gifts/', include('gifts.urls')),
    path('accounts/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', include('sendemail.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    def trigger_error(request):
        division_by_zero = 1 / 0


    urlpatterns += [path('sentry-debug/', trigger_error)]

    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
