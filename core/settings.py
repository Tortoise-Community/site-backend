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


if IS_LOCAL_DEVELOPMENT:
    CORS_ALLOWED_ORIGINS = ['https://localhost:3000']
else:
    CORS_ALLOWED_ORIGINS = [
        "https://tortoisecommunity.org",
        "https://www.tortoisecommunity.org",
        "https://api.tortoisecommunity.org",
        "https://execute.tortoisecommunity.org",
        "https://studio.tortoisecommunity.org",
    ]

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
    'core.apps.oauth',
    'core.apps.common',
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
DEFAULT_HOST = 'staff'

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


DATABASE_URL = config("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
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
AUTH_USER_MODEL = "common.User"

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
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

ENCRYPTION_SALT = config('ENCRYPTION_SALT')
ENCRYPTION_ITERATION = config('ENCRYPTION_ITERATION')


# Discord configuration for bot and verification

SERVER_ID = config('SERVER_ID')
WEBHOOK_ID = config('WEBHOOK_ID')
WEBHOOK_SECRET = config('WEBHOOK_SECRET')

OAUTH_CLIENT_ID = config('OAUTH_CLIENT_ID')
OAUTH_CLIENT_SECRET = config('OAUTH_CLIENT_SECRET')
OAUTH_REDIRECT_URI = config('OAUTH_REDIRECT_URI')

GITHUB_ACCESS_TOKEN = config('GITHUB_ACCESS_TOKEN')
