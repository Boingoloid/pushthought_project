"""
Django settings for pushthought project.
Generated by 'django-admin startproject' using Django 1.8.4.
For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import environ

PROJECT_FOLDER = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

DJANGO_APPS = [
    # Default Django apps:
    # 'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'rest_framework',
    'snippets',
    'prime',
]

LOCAL_APPS = [
    'pushthought',
    'programs',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG = bool(int(os.environ.get("DEBUG", '1')))

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///admin:main2017@localhost/main'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True



SITE_ID = 1

REGISTRATION_OPEN = True    # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = '/pushthought/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,
                                                                # and are trying to access pages requiring authentication
LOCAL_SERVER = 'http://127.0.0.1:8000/'
PUSH_THOUGHT_URL = 'www.pushthought.com/'
CURRENT_SERVER = PUSH_THOUGHT_URL

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            TEMPLATE_PATH,
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

CORS_ORIGIN_WHITELIST = (
    'pushthought.com',
    'localhost:8000',
    '127.0.0.1:8000'
)

# CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?google\.com$', )



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'django-test@mail.ru'

EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'django-test@mail.ru'
EMAIL_HOST_PASSWORD = 'Qwertyasdfgh'
EMAIL_USE_TLS = True

SERVER_EMAIL = 'server@example.com'

ADMINS = [
    ('Viacheslav', 'slava.khromyak@gmail.com'),
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allowed host headers
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['localhost','127.0.0.1','.pushthought.com','.herokuapp.com']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CONGRESS_DATA_UPDATE_TRIGGER = False

import os

TWITTER_CALLBACK_ROOT_URL = 'http://127.0.0.1:8000/verify_catch'

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = os.environ.get('SECRET_KEY'), '57464'
#
#
# # parse-server
# PARSE_APP_ID = os.environ.get('PARSE_APP_ID')
# PARSE_REST_KEY = os.environ.get('PARSE_REST_KEY')
# PARSE_MASTER = os.environ.get('PARSE_MASTER')
# PARSE_KEY = os.environ.get('PARSE_KEY')
# PARSE_SECRET = os.environ.get('PARSE_SECRET')
# PARSE_SERVER_URL = os.environ.get('PARSE_SERVER_URL')
#
# # PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'
# # app level twitter settings
# TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
# TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
# # user level twitter settings
# TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
# TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
#
# # TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'
#
# # sunlight labs api key
# SUNLIGHT_LABS_API_KEY = os.environ.get('SUNLIGHT_LABS_API_KEY')
#
# # database
# MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
# MONGODB_URI = os.environ.get('MONGODB_URI')

# SECURITY WARNING: keep the secret key used in production secret!

# from settings import settings_prod
# HORSE = settings_prod.HORSE
# print "printing horse: ", HORSE

SECRET_KEY = '9q^nt0sc2+hi%ixu*q40%1h5p$)r7+-1kmfc#mxnwp#va*l$0_'

# SECURITY WARNING: keep the secret key used in production secret!

# sunlight labs api key
SUNLIGHT_LABS_API_KEY = "ed7f6bb54edc4577943dcc588664c89f"

# database
MONGO_DBNAME = "heroku_zcdt9dml"
MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@ds037175.mlab.com:37175/heroku_zcdt9dml"

# MONGO_DBNAME = "heroku_zcdt9dml"
# MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@127.0.0.1:27017/heroku_zcdt9dml"

import socket
print "socket"

if socket.gethostname().endswith('local'):
    print "yes local"
else:
    print "no not local"
# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': False,
        # },
        'jobs': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

# parse-server
PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'
PARSE_MASTER = 'V3eewSuWRXuLoAHNv4rWOecfITxwoUVqGpNM8y0u'
PARSE_KEY = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_SECRET = 'tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP'
PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'
# PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'
# app level twitter settings
TWITTER_CONSUMER_KEY = 'uaqTefYM2ZCqquWDYVSe4kTqD'
TWITTER_CONSUMER_SECRET = 'BiN5qkDZpltqgHhyCtUO0zYrSsgE3WhTWEqYAgKhIAmpl1f4NI'
# user level twitter settings
TWITTER_ACCESS_TOKEN = '3082438601-f7UpqrzsVb9wfoUrF4pUXxdsqHm7T6Ybd2mFOFO'
TWITTER_ACCESS_TOKEN_SECRET = '7LqRKtDnG84rfmEvvS0n1cW47Zomg3uWkEjIoQAXuqWnr'
TWITTER_CALLBACK_ROOT_URL = 'http://127.0.0.1:8000/verify_catch'
# TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

# sunlight labs api key
SUNLIGHT_LABS_API_KEY = "ed7f6bb54edc4577943dcc588664c89f"

# database
MONGO_DBNAME = "heroku_zcdt9dml"
MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@ds037175.mlab.com:37175/heroku_zcdt9dml"

# MONGO_DBNAME = "heroku_zcdt9dml"
# MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@127.0.0.1:27017/heroku_zcdt9dml"

import socket
print "socket"

if socket.gethostname().endswith('local'):
    print "yes local"
else:
    print "no not local"