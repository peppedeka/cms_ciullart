from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ciullart',
        'USER': 'ciullart',
        'PASSWORD': 'ciullart',
        'HOST': 'localhost',
        'PORT': '',
    }
}

try:
    from .local import *
except ImportError:
    pass
