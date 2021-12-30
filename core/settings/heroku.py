"""
Configuration for deployment to Heroku (staging / backup for our production)
"""
from core.settings.prod import *
import dj_database_url

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://\w+\.vercel\.app$",
]

USE_X_FORWARDED_HOST = True

DATABASE_URL = os.environ.get('DATABASE_URL')
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)
DATABASES['default'].update(db_from_env)

REDIS_URL = os.environ.get('REDIS_URL')
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_MODEL_URL = os.environ.get('CELERY_MODEL_URL')
CELERY_USE_MOCK_MODEL = False

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
