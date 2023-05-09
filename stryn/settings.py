from datetime import timedelta
import os
from pathlib import Path

from decouple import config
from dj_database_url import parse as dburl

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    'stryn.herokuapp.com',
    'stryn.dokku.outboxsistemas.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'core',
    'pagamentos',
    'pedidos',
    'emails',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'djrichtextfield',
    'django_filters',
    'nested_admin',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crum.CurrentRequestUserMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:9000',
]

ROOT_URLCONF = 'stryn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'DIRS' :  [ BASE_DIR  /  "templates" ],
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
LOGIN_REDIRECT_URL = "admin"
LOGOUT_REDIRECT_URL = "login"

WSGI_APPLICATION = 'stryn.wsgi.application'


default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config(
        'DATABASE_URL', default=default_dburl, cast=dburl
    )
}

USE_AWS = config('USE_AWS', default=False, cast=bool)
if USE_AWS:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'django-stryn2' 
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    AWS_DEFAULT_ACL = None

    #STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    STATIC_HOST = "https://d120psd45kloyc.cloudfront.net" 
    STATIC_URL = STATIC_HOST + "/static/"

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, PUBLIC_MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = 'stryn.storage_backends.PublicMediaStorage' 


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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",  # noqa E501
    "PAGE_SIZE": 10,
    }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=1),
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'EMAIL': {
        'password_reset': 'emails.views_djoser.password_reset_email.PasswordResetEmail'
    }
}

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER=config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD=config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL='Hub Nova Data <hub@novadata.com.br>'
