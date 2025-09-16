import os
from datetime import timedelta
from pathlib import Path

from decouple import config
from dj_database_url import parse as dburl
from django.core.exceptions import ImproperlyConfigured  # Para falhas em vars ausentes

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
if not SECRET_KEY:
    raise ImproperlyConfigured("SECRET_KEY deve ser definida no ambiente (Railway Variables).")
    # Debug: print("SECRET_KEY carregada:", SECRET_KEY[:10] + "...")  # Teste localmente

DEBUG = config("DEBUG", default=False, cast=bool)

# ALLOWED_HOSTS: Hardcoded "*" removido; use env para hosts específicos (ex.: "web-production-ce358.up.railway.app,localhost")
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", 
    default="*",  # Fallback inseguro só para dev; remova em prod
    cast=lambda v: [host.strip() for host in v.split(",") if host.strip()]
)
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("ALLOWED_HOSTS deve ser definida no ambiente.")
# Debug: print("ALLOWED_HOSTS:", ALLOWED_HOSTS)  # Verifique logs no Railway se 403 ocorrer

INSTALLED_APPS = [
    "django_app_novadata",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "core",
    "pagamentos",
    "pedidos",
    "emails",
    "drf_spectacular",
    "rest_framework_simplejwt",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "djrichtextfield",
    "django_filters",
    "nested_admin",
    "apistripe",
    "advanced_filters",
    "django_admin_listfilter_dropdown",
    "django_object_actions",
    "import_export",
    "novadata_utils",
    "django_quill",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "crum.CurrentRequestUserMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = config("CORS_ORIGIN_ALLOW_ALL", default=True, cast=bool)  # Hardcoded True movido

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:9000",
    cast=lambda v: [url.strip() for url in v.split(",") if url.strip()]
)
# Debug: print("CORS_ALLOWED_ORIGINS:", CORS_ALLOWED_ORIGINS)  # Teste com curl para CORS errors

ROOT_URLCONF = "stryn.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/admin/"

WSGI_APPLICATION = "stryn.wsgi.application"

# DATABASES: Default local movido para env opcional
default_dburl = config("DATABASE_URL_LOCAL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}", cast=dburl)
DATABASES = {
    "default": config("DATABASE_URL", default=default_dburl, cast=dburl)
}
# Debug: from django.db import connection; print(connection.settings_dict)  # Em shell

DATA_UPLOAD_MAX_NUMBER_FIELDS = config("DATA_UPLOAD_MAX_NUMBER_FIELDS", default=1000, cast=int)

# Configuração AWS opcional
USE_AWS = config("USE_AWS", default=False, cast=bool)
if USE_AWS:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    if not AWS_ACCESS_KEY_ID:
        raise ImproperlyConfigured("AWS_ACCESS_KEY_ID deve ser definida se USE_AWS=True.")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    if not AWS_SECRET_ACCESS_KEY:
        raise ImproperlyConfigured("AWS_SECRET_ACCESS_KEY deve ser definida se USE_AWS=True.")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    if not AWS_STORAGE_BUCKET_NAME:
        raise ImproperlyConfigured("AWS_STORAGE_BUCKET_NAME deve ser definida se USE_AWS=True.")
    AWS_S3_CUSTOM_DOMAIN = config("AWS_S3_CUSTOM_DOMAIN", default=f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": config("AWS_CACHE_CONTROL", default="max-age=86400")}
    AWS_LOCATION = config("AWS_STATIC_LOCATION", default="static")
    AWS_DEFAULT_ACL = None

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

    # S3 public media settings
    PUBLIC_MEDIA_LOCATION = config("PUBLIC_MEDIA_LOCATION", default="media")
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
    DEFAULT_FILE_STORAGE = "stryn.storage_backends.PublicMediaStorage"  # Note: Ajuste se necessário

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static & media (local fallback se não usar AWS)
STATIC_URL = config("STATIC_URL", default="/static/")
STATIC_ROOT = config("STATIC_ROOT", default=str(BASE_DIR / "static"))

MEDIA_URL = config("MEDIA_URL", default="/media/")
MEDIA_ROOT = config("MEDIA_ROOT", default=str(BASE_DIR / "media"))
# Debug: print(f"STATIC_URL: {STATIC_URL}, MEDIA_URL: {MEDIA_URL}")  # Após collectstatic

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": config("REST_PAGE_SIZE", default=10, cast=int),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=config("JWT_ACCESS_LIFETIME_WEEKS", default=1, cast=int)),
}

DJOSER = {
    "PASSWORD_RESET_CONFIRM_URL": config("DJOSER_PASSWORD_RESET_URL", default="password/reset/confirm/{uid}/{token}"),
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "EMAIL": {
        "password_reset": "emails.views_djoser.password_reset_email.PasswordResetEmail"
    },
}

EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST = config("EMAIL_HOST")
if not EMAIL_HOST:
    raise ImproperlyConfigured("EMAIL_HOST deve ser definida para envios de email.")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
if not EMAIL_HOST_USER:
    raise ImproperlyConfigured("EMAIL_HOST_USER deve ser definida.")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@strynmenu.com.br")
# Debug: from django.core.mail import send_mail; send_mail('Test', 'Body', DEFAULT_FROM_EMAIL, ['test@example.com'])  # Em shell

AUTHENTICATION_BACKENDS = [
    "global_functions.authentication.LoginUsernameEmail",
]