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
import psycopg2
import urlparse

PROJECT_FOLDER = os.path.realpath(os.path.dirname(__file__))
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9q^nt0sc2+hi%ixu*q40%1h5p$)r7+-1kmfc#mxnwp#va*l$0_'

DEBUG = True


# SECURITY WARNING: don't run with debug turned on in production!

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

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pushthought',
    'corsheaders',
    'rest_framework',
    'snippets',
    'prime',
)


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
)


ROOT_URLCONF = 'pushthought.urls'

DJANGO_SETTINGS_MODULE = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': TEMPLATE_DIRS,
        'APP_DIRS': True,
        'OPTIONS': {'debug':DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pushthought.wsgi.application'


CORS_ORIGIN_WHITELIST = (
    'pushthought.com',
    'localhost:8000',
    '127.0.0.1:8000'
)

# CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(\w+\.)?google\.com$', )


# DATABASES = {
#    'default' : {
#       'ENGINE' : 'django_mongodb_engine',
#       'NAME': 'mongodb://macalin:ma99723tt@ds037175.mongolab.com:37175/heroku_zcdt9dml',
#       'USER': 'macalin',
#       'PASSWORD': 'ma99723tt',
#       'HOST': '127.0.0.1',
#       'PORT': '5432',
#    }
# }

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'd6lt20ja1h9poi',
#         'HOST': 'ec2-54-204-8-224.compute-1.amazonaws.com',
#         'PORT': '5432',
#         'USER': 'hdgnhjpsjylwrv',
#         'PASSWORD': 'WONinZmjc9PthqNGYp6mZfg8fF',
#     }
# }



# DATABASE_URL = 'postgres://hdgnhjpsjylwrv:WONinZmjc9PthqNGYp6mZfg8fF@ec2-54-204-8-224.compute-1.amazonaws.com:5432/d6lt20ja1h9poi'
#
# urlparse.uses_netloc.append("postgres")
# url = urlparse.urlparse(DATABASE_URL)
# # url = urlparse.urlparse(os.environ["DATABASE_URL"])
#
# conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
# )


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

## This is heroku code

# Parse database configuration from $DATABASE_URL
import dj_database_url
# DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['localhost','127.0.0.1','.pushthought.com','.herokuapp.com']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'

PARSE_KEY = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_SECRET = 'tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP'
PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'
# app level twitter settings
TWITTER_CONSUMER_KEY = 'uaqTefYM2ZCqquWDYVSe4kTqD'
TWITTER_CONSUMER_SECRET = 'BiN5qkDZpltqgHhyCtUO0zYrSsgE3WhTWEqYAgKhIAmpl1f4NI'
# user level twitter settings
TWITTER_ACCESS_TOKEN = '3082438601-f7UpqrzsVb9wfoUrF4pUXxdsqHm7T6Ybd2mFOFO'
TWITTER_ACCESS_TOKEN_SECRET = '7LqRKtDnG84rfmEvvS0n1cW47Zomg3uWkEjIoQAXuqWnr'
TWITTER_CALLBACK_ROOT_URL = 'http://127.0.0.1:8000/verify_catch'

SUNLIGHT_LABS_API_KEY = "ed7f6bb54edc4577943dcc588664c89f"

MONGO_DBNAME = "heroku_zcdt9dml"
MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@ds037175.mlab.com:37175/heroku_zcdt9dml"

CONGRESS_DATA_UPDATE_TRIGGER = False



# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'mysite.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#         'MYAPP': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     }
# }

# shell script for creating objects - just a note -----------------------------------------
# >>> from books.models import Publisher
# >>> p1 = Publisher(name='Apress', address='2855 Telegraph Avenue',
# ...     city='Berkeley', state_province='CA', country='U.S.A.',
# ...     website='http://www.apress.com/')
# >>> p1.save()
# >>> p2 = Publisher(name="O'Reilly", address='10 Fawcett St.',
# ...     city='Cambridge', state_province='MA', country='U.S.A.',
# ...     website='http://www.oreilly.com/')
# >>> p2.save()
# >>> publisher_list = Publisher.objects.all()
# >>> publisher_list
# [<Publisher: Publisher object>, <Publisher: Publisher object>]