from django.contrib import admin
from django.urls import path, include
from adverts import views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('djga/', include('google_analytics.urls')),   # This line for Django versions >=2.0
    path('select2/', include("django_select2.urls")),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('', include('sendemail.urls')),
    path('search', views.SearchView.as_view(), name="global_search"),
    path('jobs/', include('jobs.urls')),
    path('rents/', include('rents.urls')),
    path('items/', include('items.urls')),
    path('gifts/', include('gifts.urls')),
    path('accounts/', include('accounts.urls')),
    path('cookie-policy', TemplateView.as_view(template_name='policy/cookie_policy.html'), name='cookie'),
    path('privacy-policy', TemplateView.as_view(template_name='policy/privacy_policy.html'), name='privacy'),
    path('term-of-services', TemplateView.as_view(template_name='policy/term_of_services.html'), name='term'),
    path('checkout', include('shop.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    def trigger_error():
        return 1 / 0

    urlpatterns += [path('sentry-debug/', trigger_error)]

    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
