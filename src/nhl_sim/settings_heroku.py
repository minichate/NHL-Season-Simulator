from settings import *
import dj_database_url

DATABASES['default'] =  dj_database_url.config()

BROKER_URL = os.environ['REDISTOGO_URL']
CELERY_RESULT_BACKEND = os.environ['REDISTOGO_URL']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')