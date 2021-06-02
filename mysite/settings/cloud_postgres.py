from .base import *
from decouple import config

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_IP'),
        'PORT': config('DB_PORT', default='5432'),
        'ATOMIC_REQUESTS': True
    }
}
