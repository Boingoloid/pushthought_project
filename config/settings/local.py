from .base import *
# from .secret import *

# SECURITY WARNING: don't run with debug turned on in production!
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'main',
        'USER': 'admin',
        'PASSWORD': 'admin2017',
        'HOST': 'localhost',
        'PORT': '',
    }
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

DJANGO_APPS += [
    'whitenoise.runserver_nostatic',
]

PARSE_APP_ID = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_REST_KEY = 'YTeYDL8DeSDNsmZT219Lp8iXgPZ24ZGu3ywUjo23'
PARSE_MASTER = 'V3eewSuWRXuLoAHNv4rWOecfITxwoUVqGpNM8y0u'
PARSE_KEY = 'lzb0o0wZHxbgyIHSyZLlooijAK9afoyN8RV4XwcM'
PARSE_SECRET = 'tHZLsIENdHUpZXlfG1AZVLXsETYbgvr5lUorFegP'

PARSE_SERVER_URL = 'ptparsedev.herokuapp.com'
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
MONGO_DBNAME = "heroku_zcdt9dml" #prod
MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@ds037175.mlab.com:37175/heroku_zcdt9dml"
# MONGO_DBNAME = "heroku_tz491rn8"
# MONGODB_URI = "mongodb://part_elf_part_man:all_boingo@ds159050.mlab.com:59050/heroku_tz491rn8"
SECRET_KEY = '9q^nt0sc2+hi%ixu*q40%1h5p$)r7+-1kmfc#mxnwp#va*l$0_'

ALLOWED_HOSTS = ['*']

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 86400 # sec
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_NAME = 'DSESSIONID'
SESSION_COOKIE_SECURE = False


SITE_ID = 1

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGGING['handlers']['mail_admins']['class'] = 'logging.NullHandler'
