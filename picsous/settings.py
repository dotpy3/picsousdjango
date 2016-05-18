# coding: utf-8

"""
Django settings for picsous project.

Generated by 'django-admin startproject' using Django 1.9.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yi_gm6l60o-pk5uts_^o)jw^kfsbq@39w9n2+vo&o1ss^9$qod'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_extensions',
    'constance',
    'constance.backends.database',
    'utcaccounts',
    'perm',
    'facture',
    'core',
]

REST_FRAMEWORK = {
    'DATETIME_FORMAT': None,  # serializers returns datetime objects
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

CONSTANCE_CONFIG = {
    'GINGER_URL': ('https://assos.utc.fr/ginger/v1/', 'Adresse de connexion à Ginger.', str),
    'GINGER_KEY': ('', 'Clé de connexion à Ginger', str),
    'NEMOPAY_CONNECTION_UID': ('00000000', 'UID de l\'utilisateur dont les droits sont utilisés'
                                           'pour la connexion à PayUTC. Doit avoir les droits'
                                           'GESARTICLE et TRESO.', str),
    'NEMOPAY_CONNECTION_PIN': (0000, 'PIN de l\'utilisateur dont les droits sont utilisés'
                                     'pour la connexion à PayUTC.', int),
    'NEMOPAY_API_KEY': ('', 'Clé d\'application permettant de se connecter à PayUTC.', str),
    'NEMOPAY_API_URL': ('https://api.nemopay.net/services/', 'Adresse permettant de se connecter à PayUTC.', str),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'picsous.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'facture/templates')],
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

AUTHENTICATION_BACKENDS = (
    'core.services.payutc.PayUTCAuthBackend',
)

WSGI_APPLICATION = 'picsous.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'facture/static'),
)

NEMOPAY_API_URL = 'https://api.nemopay.net/services/'
NEMOPAY_API_KEY = '' # to be defined in local_settings.py
NEMOPAY_SYSTEM_ID = 'payutc'
NEMOPAY_FUNDATION_ID = 2
NEMOPAY_LOGIN_ACTIVATED = True
NEMOPAY_LOGIN_SERVICE = 'POSS3'
NEMOPAY_ARTICLES_CATEGORY = 14

NEMOPAY_CONNECTION_UID = '00000000'
NEMOPAY_CONNECTION_PIN = 0000

GINGER_ACTIVATED = True
GINGER_URL = 'https://assos.utc.fr/ginger/v1/'
GINGER_KEY = '' # to be defined in local_settings.py

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = ''

CORS_ORIGIN_ALLOW_ALL = False

try:
    from local_settings import *
except ImportError:
    pass
