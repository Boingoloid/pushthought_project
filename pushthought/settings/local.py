from .base import *
# from .secret import *



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
SECRET_KEY = '9q^nt0sc2+hi%ixu*q40%1h5p$)r7+-1kmfc#mxnwp#va*l$0_'