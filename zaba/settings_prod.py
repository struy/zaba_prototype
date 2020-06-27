from .settings import *
from .settings import env

PROD_APPS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT')
    },
}

GOOGLE_ANALYTICS = {
    'google_analytics_id': env('DJANGO_GOOGLE_ANALYTICS'),
}

INSTALLED_APPS += PROD_APPS
