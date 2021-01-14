import importlib
import os
import re

import pytz


DEPLOY_ENV = os.environ.get('DEPLOY', 'dev')
if DEPLOY_ENV not in ('live', 'test', 'dev'):
    DEPLOY_ENV = 'dev'  # Whatever other environment, just use test XDD

REGION = os.environ.get('EVENT_REGION')

_COOKIE_DOMAIN = os.environ.get('DOMAIN')
if DEPLOY_ENV != 'live':
    _COOKIE_DOMAIN = DEPLOY_ENV + '-' + _COOKIE_DOMAIN

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROJECT_ROOT = os.path.abspath(os.path.join(_BASE_DIR, '..', '..'))


CUSTOM_DNS_DOMAINS = []

SECRET_KEY = '8aabe5d3O7a_'
DEBUG = DEPLOY_ENV != 'live'
TEST = DEPLOY_ENV == 'test'
DOMAIN = _COOKIE_DOMAIN

ALLOWED_HOSTS = [
    DOMAIN, 'https://hsun-shorter.herokuapp.com/',
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'utils.middlewares.gto_exception.GTOExceptionMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.messages',
    'social_django',
    'django_www',
)

ROOT_URLCONF = 'django_www.urls'
WSGI_APPLICATION = 'django_www.wsgi.application'

if DEPLOY_ENV == 'dev':
    INSTALLED_APPS += (
        'django.contrib.staticfiles',  # needed to be able to collect static files
    )

STATIC_URL = '/django-static/'  # url to access the admin related static files
STATIC_ROOT = os.path.join(_PROJECT_ROOT, 'static')  # under which the collected admin/ static file folder will be located

# Sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_DOMAIN = _COOKIE_DOMAIN
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = (DEPLOY_ENV != 'dev')
CSRF_COOKIE_SECURE = (DEPLOY_ENV != 'dev')

# Internationalization
LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
TIME_ZONE = os.environ.get('TIME_ZONE')
CURRENT_TZ = pytz.timezone(TIME_ZONE)
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Logging
_LOG_FILE = os.path.join(_BASE_DIR, '..', 'logs', 'django.log')
LOGGING = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(levelname)s|%(asctime)s|%(pathname)s|%(funcName)s|l-%(lineno)s|%(message)s',
        },
    },
    'handlers': {
        'all': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': _LOG_FILE,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['all'],
            'level': 'INFO',
        },
    },
}

# add logger for mysql queries
if DEBUG:
    _LOG_SQL_FILE = os.path.join(_BASE_DIR, '..', 'logs', 'django_sql.log')
    LOGGING['handlers']['sql_file'] = {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': _LOG_SQL_FILE,
        'maxBytes': 100*1024*1024,
        'backupCount': 5,
        'formatter': 'standard',
        'encoding': 'utf-8',
    }
    LOGGING['loggers']['default']['propagate'] = True
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['sql_file'],
        'level': 'DEBUG',
    }
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
            'loaders': ['django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader'],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'prompt': 'select_account'}

DATABASE_ROUTERS = ['utils.db.DatabaseRouter']

USE_CACHE = 1
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

local_config = importlib.import_module('django_www.settings.' + DEPLOY_ENV)
locals().update(local_config.__dict__)
