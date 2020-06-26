from .settings import *
from .settings import env

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

# ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=["13.59.235.149"])
