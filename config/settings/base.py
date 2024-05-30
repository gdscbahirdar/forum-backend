import os
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def rel(*path):
    """
    Used to get the relative path for any file, combines with the BASEDIR
    @param path: the relative path for the file
    @return: absolute path to the file
    """
    return os.path.join(BASE_DIR, *path)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "phonenumber_field",
    "storages",
]
LOCAL_APPS = [
    "apps.common",
    "apps.users",
    "apps.rbac",
    "apps.entities",
    "apps.forum",
    "apps.resources",
    "apps.badges",
    "apps.services",
    "apps.content_actions",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [rel("templates/")],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOSTNAME"),
        "PORT": config("DB_PORT", cast=int),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "apps.common.validators.CustomPasswordValidator",
    },
]

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

USE_SPACES = config("USE_SPACES", default=False, cast=bool)

if False:
    AWS_ACCESS_KEY_ID = config("STATIC_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("STATIC_SECRET_KEY")
    AWS_STORAGE_BUCKET_NAME = config("STATIC_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = config("STATIC_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_LOCATION = "static"
    AWS_DEFAULT_ACL = "public-read"
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {"location": "media", "file_overwrite": False, "default_acl": "public-read"},
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {"location": "static", "default_acl": "public-read"},
        },
    }
    AWS_QUERYSTRING_AUTH = False
    STATIC_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com"
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/media/"
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = rel("staticfiles")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = rel("media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=Csv())

# Email
EMAIL_BACKEND = config("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# Admin
ADMIN_URL = config("DJANGO_ADMIN_URL", default="admin/")

# Page size
PAGE_SIZE = config("PAGE_SIZE", default=30, cast=int)
MAX_PAGE_SIZE = config("MAX_PAGE_SIZE", default=100, cast=int)

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": ("apps.common.pagination.DynamicPageSizePagination"),
    "PAGE_SIZE": PAGE_SIZE,
    "ORDERING_PARAM": "sort",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# dj-rest-auth
# -------------------------------------------------------------------------------
# dj-rest-auth - https://dj-rest-auth.readthedocs.io/en/latest/configuration.html#configuration
REST_AUTH = {
    "USER_DETAILS_SERIALIZER": "apps.users.serializers.CustomUserDetailsSerializer",
    "OLD_PASSWORD_FIELD_ENABLED": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "JWT_AUTH_RETURN_EXPIRATION": True,
    "JWT_AUTH_COOKIE": "forum-access-token",
    "JWT_AUTH_REFRESH_COOKIE": "forum-refresh-token",
}

# simple-jwt
# -------------------------------------------------------------------------------
# simple-jwt - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config("ACCESS_TOKEN_LIFETIME", cast=int)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config("REFRESH_TOKEN_LIFETIME", cast=int)),
}

# drf-spectacular
# -------------------------------------------------------------------------------
# drf-spectacular - https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
    "TITLE": "An Online Discussion Forum for BiT",
    "DESCRIPTION": "An Online Discussion Forum for BiT aims to leverage digital solutions to facilitate more effective communication, resource sharing, and collaborative learning among students and faculty. By integrating advanced technological features, the forum is designed not only to complement the existing educational framework but also to expand the avenues through which students and faculty engage, innovate, and excel in their academic and professional pursuits.",  # noqa E501
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Phone Number
# ------------------------------------------------------------------------------
# https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#settings
PHONENUMBER_DEFAULT_REGION = "ET"
PHONENUMBER_DEFAULT_FORMAT = "NATIONAL"
