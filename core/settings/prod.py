"""
INCOMPLETE Configuration for deployment
"""
from core.settings.base import *

# set SECRET_KEY for production
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# add heroku app url or create env var with url
ALLOWED_HOSTS = [os.environ.get("PRODUCTION_HOST")]

# debug has to be false in production
DEBUG = False

# cors headers configuration
CORS_ALLOWED_ORIGINS = [

]

INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

# whitenoise middleware - has to be first in the list
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# directory to which Django will move those static assets and from which it will serve them when the app is running
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_URL = "/static/"

# database url
DATABASE_URL = os.environ.get('DATABASE_URL')

# db config
PROD_DB = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': ''
}

DATABASES['default'].update(PROD_DB)

# Redis channel layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', ('127.0.0.1', 6379))],
        },
    },
}
