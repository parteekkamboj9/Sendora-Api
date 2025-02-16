from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# Local-specific settings like database connection for development
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
# REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.AdminRenderer')

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:3000', 'http://localhost:3000']
