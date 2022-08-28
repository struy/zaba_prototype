from .settings import *

REDIS_HOST = 'redis'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# CELERY
BROKER_URL = f'redis://{REDIS_HOST}:6379'
CELERY_RESULT_BACKEND = 'redis://{REDIS_HOST}:6379'

POSTGRES_HOST = 'db'
POSTGRES_PORT = 5432
POSTGRES_DB = 'db_name'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'postgres'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT
    },
}
