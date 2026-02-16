import logging
import os
import sys

from pathlib import Path


logging.captureWarnings(True)


# Website's name
SITE_NAME = "Ratingswiz"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0peo@#x64ur3!h$ryje!$8e9xww8s1r66jx!%*#ythg&jmozf2"

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Allowed hosts
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',
    '127.0.0.1',
    '.example.com',
]


# Application definition
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    # Third-party
    "allauth",
    "allauth.account",
    "crispy_forms",
    "crispy_bootstrap5",
    "debug_toolbar",
    # Local
    "apps.accounts",
    "apps.pages",
    "apps.ratinglists",
]


# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Django Debug Toolbar
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # django-allauth
]


# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'


# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # "DIRS": [BASE_DIR / "templates"],
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

# https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = "UTC"

# https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-USE_I18N
USE_I18N = True

# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [BASE_DIR / "locale"]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files

# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = 'static/'

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    BASE_DIR / "apps/accounts/static/",
    BASE_DIR / "apps/pages/static/",
    BASE_DIR / "apps/ratinglists/static/",
    BASE_DIR / "static",
]

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "staticfiles"

# https://whitenoise.readthedocs.io/en/latest/django.html
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Media files

# MEDIA_URL is the URL we can use in our templates for the files
MEDIA_URL = '/media/'

# MEDIA_ROOT is the absolute filesystem path to the directory for user-uploaded files
# MEDIA_ROOT = BASE_DIR / "media/"
MEDIA_ROOT = "/home/treetop/appmedia/ratingswizmain/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# django-crispy-forms
# https://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Make django-crispy-forms fail loud
# By default when crispy-forms encounters errors, it fails silently, logs them and
# continues working if possible. Raise exceptions instead of logging, telling you what’s
# going on when you are developing in debug mode.
# https://django-crispy-forms.readthedocs.io/en/2.3/crispy_tag_forms.html#make-crispy-forms-fail-loud
CRISPY_FAIL_SILENTLY = not DEBUG


# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = "root@localhost"


# The django-debug-toolbar is shown only if your IP address is listed in Django's
# INTERNAL_IPS setting.
# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-INTERNAL_IPS
# https://django-debug-toolbar.readthedocs.io/en/latest/index.html
INTERNAL_IPS = [
    "127.0.0.1",
    '0.0.0.0',
    '192.168.43.198',
    '192.168.1.4',
]


# Custom user model
# AUTH_USER_MODEL = 'accounts.CustomUser'  # new custom user setting
# AUTH_USER_MODEL = 'apps.accounts.Account'  # new custom user setting
# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'accounts.Account'  # new custom user setting


# django-allauth config
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1


# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/views.html#logout-account-logout
ACCOUNT_LOGOUT_REDIRECT_URL = "home"

# https://django-allauth.readthedocs.io/en/latest/installation.html?highlight=backends
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True


# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",  # Default Django dev server
    "http://127.0.0.1:8000",  # Alternative local address
    'http://0.0.0.0:8000',
]


# Email server configuration
# Use Google’s SMTP server with a standard Gmail account
# Sending emails with Django - Django 4 By Example - Mele A.
# https://support.google.com/accounts/answer/185833
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Resource Usage Limits
STORAGE_MAX = 4  # Gigabytes
RAM_MAX = 256  # Megabytes
CPU_MAX = 400  # Megahertz


# Celery - Distributed Task Queue
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
# Configure Celery to use Redis as message broker.
CELERY_BROKER_URL = "redis://redis:6379/0"

# Celery workers may leak the memory, eventually depriving the instance of resources.
# This setting forces celery to stop worker, clean after it, and create new one
# after worker has processed 10 tasks.
CELERY_WORKER_MAX_TASKS_PER_CHILD = 10


ALLOWED_CLIENTS = [
    '127.0.0.1',
    'Chrome',
    'Curl',
    'Firefox',
    'Mozilla',
]


FIDE_FEDERATIONS = [
    {"name":"Algeria", "code":"ALG", "region": "africa"},
    {"name":"Angola", "code":"ANG", "region": "africa"},
    {"name":"Botswana", "code":"BOT", "region": "africa"},
    {"name":"Burkina Faso", "code":"BUR", "region": "africa"},
    {"name":"Burundi", "code":"BDI", "region": "africa"},
    {"name":"Cameroon", "code":"CMR", "region": "africa"},
    {"name":"Cape Verde", "code":"CPV", "region": "africa"},
    {"name":"Central African Republic", "code":"CAF", "region": "africa"},
    {"name":"Chad", "code":"CHA", "region": "africa"},
    {"name":"Comoros Islands", "code":"COM", "region": "africa"},
    {"name":"Côte d’Ivoire", "code":"CIV", "region": "africa"},
    {"name":"Democratic Republic of the Congo", "code":"COD", "region": "africa"},
    {"name":"Djibouti", "code":"DJI", "region": "africa"},
    {"name":"Egypt", "code":"EGY", "region": "africa"},
    {"name":"Equatorial Guinea", "code":"GEQ", "region": "africa"},
    {"name":"Eritrea", "code":"ERI", "region": "africa"},
    {"name":"Eswatini", "code":"SWZ", "region": "africa"},
    {"name":"Ethiopia", "code":"ETH", "region": "africa"},
    {"name":"Gabon", "code":"GAB", "region": "africa"},
    {"name":"Gambia", "code":"GAM", "region": "africa"},
    {"name":"Ghana", "code":"GHA", "region": "africa"},
    {"name":"Guinea", "code":"ZZZ", "region": "africa"},
    {"name":"Kenya", "code":"KEN", "region": "africa"},
    {"name":"Lesotho", "code":"LES", "region": "africa"},
    {"name":"Liberia", "code":"LBR", "region": "africa"},
    {"name":"Libya", "code":"LBA", "region": "africa"},
    {"name":"Madagascar", "code":"MAD", "region": "africa"},
    {"name":"Malawi", "code":"MAW", "region": "africa"},
    {"name":"Mali", "code":"MLI", "region": "africa"},
    {"name":"Mauritania", "code":"MTN", "region": "africa"},
    {"name":"Mauritius", "code":"MRI", "region": "africa"},
    {"name":"Morocco", "code":"MAR", "region": "africa"},
    {"name":"Mozambique", "code":"MOZ", "region": "africa"},
    {"name":"Namibia", "code":"NAM", "region": "africa"},
    {"name":"Niger", "code":"NIG", "region": "africa"},
    {"name":"Nigeria", "code":"NGR", "region": "africa"},
    {"name":"Rwanda", "code":"RWA", "region": "africa"},
    {"name":"Sao Tome and Principe", "code":"STP", "region": "africa"},
    {"name":"Senegal", "code":"SEN", "region": "africa"},
    {"name":"Seychelles", "code":"SEY", "region": "africa"},
    {"name":"Sierra Leone", "code":"SLE", "region": "africa"},
    {"name":"Somalia", "code":"SOM", "region": "africa"},
    {"name":"South Africa", "code":"RSA", "region": "africa"},
    {"name":"South Sudan", "code":"SSD", "region": "africa"},
    {"name":"Sudan", "code":"SUD", "region": "africa"},
    {"name":"Tanzania", "code":"TAN", "region": "africa"},
    {"name":"Togo", "code":"TOG", "region": "africa"},
    {"name":"Tunisia", "code":"TUN", "region": "africa"},
    {"name":"Uganda", "code":"UGA", "region": "africa"},
    {"name":"Zambia", "code":"ZAM", "region": "africa"},
    {"name":"Zimbabwe", "code":"ZIM", "region": "africa"},
]

