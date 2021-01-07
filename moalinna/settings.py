"""
Django settings for moalinna project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from . import config_reader

################################################################################
## Section: general

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = config_reader.open_config_file(BASE_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('general', 'SECRET_KEY', fallback='s)v4%=pyxk*fue=vce60bx3r01e9vl4%9^b%(l=p_665mm_d@+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('general', 'DEBUG', fallback=True)

################################################################################
## Section: server

ALLOWED_HOSTS = [
    config.get('server', 'HOST')
] if config.has_option('server', 'HOST') else []

if config.has_option('server', 'FORCE_SCRIPT_NAME'):
    FORCE_SCRIPT_NAME = '/' + config.get('server', 'FORCE_SCRIPT_NAME').lstrip('/')
else:
    FORCE_SCRIPT_NAME = None

def prefix_script_name(url):
    return (FORCE_SCRIPT_NAME or '') + url

if config.getboolean('server', 'TRUST_X_FORWARDED_PROTO', fallback=False):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'authorized_keys.apps.AuthorizedKeysConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moalinna.urls'

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

WSGI_APPLICATION = 'moalinna.wsgi.application'


################################################################################
## Section: database

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


################################################################################
## Section: login

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

LOGIN_URL = prefix_script_name('/login/')

LOGIN_REDIRECT_URL = prefix_script_name('/')
LOGOUT_REDIRECT_URL = prefix_script_name('/')

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

OIDC_ENABLED = config.has_option('login', 'OIDC_ENDPOINT')

if OIDC_ENABLED:
    OIDC_ENDPOINT = config.get('login', 'OIDC_ENDPOINT').rstrip('/')

    OIDC_OP_AUTHORIZATION_ENDPOINT = OIDC_ENDPOINT + '/auth'
    OIDC_OP_TOKEN_ENDPOINT = OIDC_ENDPOINT + '/token'
    OIDC_OP_USER_ENDPOINT = OIDC_ENDPOINT + '/me'
    OIDC_OP_JWKS_ENDPOINT = OIDC_ENDPOINT + '/certs'

    if config.has_option('login', 'OIDC_RP_SIGN_ALGO'):
        OIDC_RP_SIGN_ALGO = config.get('login', 'OIDC_RP_SIGN_ALGO')

    OIDC_RP_CLIENT_ID = config.get('login', 'OIDC_CLIENT_ID')
    OIDC_RP_CLIENT_SECRET = config.get('login', 'OIDC_CLIENT_SECRET')

    INSTALLED_APPS += ['mozilla_django_oidc']
    AUTHENTICATION_BACKENDS += [
        'moalinna.auth.OIDCAuthenticationBackend',
    ]
    MIDDLEWARE += [
        'mozilla_django_oidc.middleware.SessionRefresh',
    ]


################################################################################
## Section: i18n

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = config.get('i18n', 'LANGUAGE_CODE', fallback='en-us')

TIME_ZONE = config.get('i18n', 'TIME_ZONE', fallback='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = prefix_script_name('/static/')

# Bulma/Bootstrap CSS use 'danger' as red color tag instead of 'error'

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.ERROR: 'danger'
}
