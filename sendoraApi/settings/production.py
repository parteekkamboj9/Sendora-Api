from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

# Production-specific settings
DATABASES['default'] = {
    'ENGINE': os.environ['PRODUCTION_DB_ENGINE'],
    'NAME': os.getenv('PRODUCTION_DB_NAME'),
    'USER': os.getenv('PRODUCTION_DB_USER'),
    'PASSWORD': os.getenv('PRODUCTION_DB_PASSWORD'),
    'HOST': os.getenv('PRODUCTION_DB_HOST'),
    'PORT': os.getenv('PRODUCTION_DB_PORT'),
}
