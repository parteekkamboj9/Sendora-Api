from .base import *

DEBUG = False
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(' ')

# Staging-specific database or settings
DATABASES['default'] = {
    'ENGINE': os.environ['STAGING_DB_ENGINE'],
    'NAME': os.getenv('STAGING_DB_NAME'),
    'USER': os.getenv('STAGING_DB_USER'),
    'PASSWORD': os.getenv('STAGING_DB_PASSWORD'),
    'HOST': os.getenv('STAGING_DB_HOST'),
    'PORT': os.getenv('STAGING_DB_PORT'),
}
