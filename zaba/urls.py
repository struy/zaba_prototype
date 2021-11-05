from django.contrib import admin
from django.urls import path, include
from apps.adverts import views
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

from apps.adverts.views import robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('djga/', include('google_analytics.urls')),   # This line for Django versions >=2.0
    path('select2/', include("django_select2.urls")),
    path("robots.txt", robots_txt),
]

urlpatterns += i18n_patterns(
    path('', views.home, name='home'),
    path('', include('apps.sendemail.urls')),
    path('', include('apps.adverts.urls')),
    path('search', views.SearchView.as_view(), name="global_search"),
    path('jobs/', include('apps.jobs.urls')),
    path('rents/', include('apps.rents.urls')),
    path('items/', include('apps.items.urls')),
    path('gifts/', include('apps.gifts.urls')),
    path('services/', include('apps.services.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('cookie-policy/', TemplateView.as_view(template_name='policy/cookie_policy.html'), name='cookie'),
    path('about-us/', TemplateView.as_view(template_name='policy/about_us.html'), name='about_us'),
    path('privacy-policy/', TemplateView.as_view(template_name='policy/privacy_policy.html'), name='privacy'),
    path('term-of-services/', TemplateView.as_view(template_name='policy/term_of_services.html'), name='term'),
    path('place-ad/', TemplateView.as_view(template_name='place_ad.html'), name='place_ad'),
    path('checkout/', include('apps.shop.urls')),
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
