from settings import *

import heroku

cloud = heroku.from_key('e7605a0ee08cf20e3867f1f1a0ac0486e32d1cb9')
app = cloud.apps['nhlplayoffscheer']

print app.config

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd5s0sml2ufd7fj',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'jykcymkzohwwtd',
        'PASSWORD': 'bpk6jBH0MvMMY6OBz_SWK2T_yt',
        'HOST': 'ec2-54-225-69-193.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}

BROKER_URL = app.config.data['REDISTOGO_URL']
CELERY_RESULT_BACKEND = app.config.data['REDISTOGO_URL']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')