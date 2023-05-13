from decouple import config
from .base import *




# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'test-topupfpl.onrender.com',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]






