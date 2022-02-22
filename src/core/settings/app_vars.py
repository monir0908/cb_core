import os

# django vars
AUTH_USER_MODEL = 'user.User'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = False
STATIC_URL = '/static/'

# env
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = int(os.environ.get('DB_PORT'))

REDIS_HOST = os.environ.get('REDIS_HOST')
RABBITMQ_URL = os.environ.get('RABBITMQ_URL')
AUTH_HOST = os.environ.get('AUTH_HOST')
# request setup
REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 8))
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.environ.get('SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET')
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
