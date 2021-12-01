"""
Configuration for production
"""
from core.settings.base import *

# set SECRET_KEY for production
SECRET_KEY = os.environ.get("SECRET_KEY")

# add backend host
ALLOWED_HOSTS = [
    os.environ.get("BACKEND_HOST")
]

# debug has to be false in production
DEBUG = False

# cors headers configuration
CORS_ALLOW_CREDENTIALS = True

# accept external calls only from frontend
CORS_ALLOWED_ORIGINS = [
    os.environ.get('FRONTEND_URL'),
]

# not sure if needed
INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

# whitenoise middleware - has to be first in the list
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# whitenoise - type of storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# directory to which Django will move those static assets and from which it will serve them when the app is running
STATIC_ROOT = os.environ.get('STATIC_ROOT')

STATIC_URL = "/static/"     # not used but should be declared anyway

# directory to which recordings will be uploaded
MEDIA_ROOT = os.environ.get('MEDIA_ROOT')

# db config
PROD_DATABASE = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'HOST': os.environ.get('DB_HOST'),
    'PORT': os.environ.get('DB_PORT'),
}
DATABASES['default'].update(PROD_DATABASE)

# Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_AUTH_PASSWORD = os.environ.get('REDIS_AUTH_PASSWORD')

# Redis as broker, result backend (Celery + Redis)
REDIS_URL = f'redis://:{REDIS_AUTH_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_MODEL_URL = os.environ.get('CELERY_MODEL_URL')
CELERY_USE_MOCK_MODEL = False

# Redis channel layers (Django Channels + Redis)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                REDIS_URL
            ],
        },
    },
}
