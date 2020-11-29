import os
import sys
import environ
import redis
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from braintree import Configuration, Environment
from django.utils.translation import gettext_lazy as _

env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env.read_env(str(BASE_DIR + "/" + ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS')

# Google Recaptcha
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = 0.7

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (len(sys.argv) >= 2 and sys.argv[1] == 'runserver')

if DEBUG:
    THUMBNAIL_DEBUG = True
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "*"]
    SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Application definition
DJANGO_APPS = ['django.contrib.admin',
               'django.contrib.auth',
               'django.contrib.contenttypes',
               'django.contrib.sessions',
               'django.contrib.messages',
               'django.contrib.staticfiles',
               'django.contrib.humanize',
               'django.contrib.gis',
               'django.contrib.sites',
               ]

THIRD_PARTY_APPS = ['django_countries',
                    'django_extensions',
                    'django_tables2',
                    'captcha',
                    'crispy_forms',
                    'sorl.thumbnail',
                    'cookielaw',
                    'mptt',
                    'language_flags',
                    'rosetta',
                    'debug_toolbar',
                    'social_django',
                    'google_analytics',
                    'django_select2',
                    'django_filters',
                    'django_cleanup.apps.CleanupConfig',
                    ]

LOCAL_APPS = ['accounts.apps.AccountsConfig',
              'adverts.apps.AdvertsConfig',
              'rents.apps.RentsConfig',
              'jobs.apps.JobsConfig',
              'items.apps.ItemsConfig',
              'gifts.apps.GiftsConfig',
              'sendemail.apps.SendemailConfig',
              'shop.apps.ShopConfig',
              ]

INSTALLED_APPS = ['modeltranslation', ] + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'

SITE_ID = 1

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'home'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # my
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'zaba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'zaba.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

INTERNAL_IPS = ['127.0.0.1']

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
    ('pl', 'Polish'),
    ('uk', 'Ukrainian'),
)

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

COUNTRIES_ONLY = [
    ('UA', _('Ukrainian')),
    ('RU', _('Russian')),
    ('PL', _('Polish')),
    ('US', _('English')),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru', 'pl', 'uk')

MODELTRANSLATION_TRANSLATION_FILES = (
    'gifts.translation', 'jobs.translation',)

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

POOL = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SELECT2_CACHE_BACKEND = "select2"

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# CELERY
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_ALWAYS_EAGER


sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    # integrations=[DjangoIntegration()],
    integrations=[RedisIntegration()],

    # temporary fix
    # transport=print,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

BRAINTREE_MERCHANT_ID = env('BRAINTREE_MERCHANT_ID')
BRAINTREE_PUBLIC_KEY = env('BRAINTREE_PUBLIC_KEY')
BRAINTREE_PRIVATE_KEY = env('BRAINTREE_PRIVATE_KEY')

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

GOOGLE_ANALYTICS = {
    'google_analytics_id': env('DJANGO_GOOGLE_ANALYTICS'),
}
