import os

import dj_database_url
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG')

IS_LOCAL_DEVELOPMENT = config('IS_LOCAL_DEVELOPMENT')

if IS_LOCAL_DEVELOPMENT:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['.tortoisecommunity.org']


CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://tortoisecommunity.org",
    "https://www.tortoisecommunity.org",
    "https://api.tortoisecommunity.org",
    "https://execute.tortoisecommunity.org",
    "https://studio.tortoisecommunity.org",
]
if IS_LOCAL_DEVELOPMENT:
    CORS_ALLOWED_ORIGINS.extend(
        ['http://localhost:3000',
         r"^http://([a-z0-9-]+\.)?localhost\.co:3000",
         "http://127.0.0.1:3000"
         ]
    )

DATE_INPUT_FORMATS = ['%Y-%m-%d']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_hosts',
    'rest_framework',
    'rest_framework.authtoken',
    'core.apps.web',
    'core.apps.ide',
    'core.apps.api'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'core.urls'
ROOT_HOSTCONF = 'core.hosts'
DEFAULT_HOST = 'web'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
# SECURE_SSL_REDIRECT = 'True'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Django rest framework Settings
# https://www.django-rest-framework.org/

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (

        'rest_framework.permissions.IsAuthenticated',

    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )

}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'core/assets')
MEDIA_ROOT = os.path.join(BASE_DIR, 'core/media')
MEDIA_URL = '/media/'


# Mail Transfer Module Handlers
# https://docs.djangoproject.com/en/3.0/topics/email/

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tortoisecommunity@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_TOKEN')
EMAIL_USE_TLS = True

HASH_SALT = config('HASH_SALT')
HASH_ITERATION = config('HASH_ITERATION')


# Discord configuration for bot and verification

SERVER_ID = config('SERVER_ID')
WEBHOOK_ID = config('WEBHOOK_ID')
WEBHOOK_SECRET = config('WEBHOOK_SECRET')

OAUTH_CLIENT_ID = config('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = config('OAUTH_CLIENT_SECRET')

GITHUB_ACCESS_TOKEN = config('GITHUB_ACCESS_TOKEN')
