from .base import *
from .heroku import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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

print "no not local ", os.environ.get('PARSE_APP_ID')



# parse-server
PARSE_APP_ID = os.environ.get('PARSE_APP_ID')
PARSE_REST_KEY = os.environ.get('PARSE_REST_KEY')
PARSE_MASTER = os.environ.get('PARSE_MASTER')
PARSE_KEY = os.environ.get('PARSE_KEY')
PARSE_SECRET = os.environ.get('PARSE_SECRET')
PARSE_SERVER_URL = os.environ.get('PARSE_SERVER_URL')

# PARSE_SERVER_URL = 'https://ptparse.herokuapp.com/parse'
# app level twitter settings
TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
# user level twitter settings
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

# TWITTER_CALLBACK_ROOT_URL = 'http://www.pushthought.com/verify_catch'

# sunlight labs api key
SUNLIGHT_LABS_API_KEY = os.environ.get('SUNLIGHT_LABS_API_KEY')

# database
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')
MONGODB_URI = str(os.environ.get('MONGODB_URI'))
SECRET_KEY = os.environ.get('SECRET_KEY')