import os

ENVIRONMENT = os.getenv('DJANGO_ENV', 'local')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'staging':
    from .staging import *
else:
    from .local import *
