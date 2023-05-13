from .base import *



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATIC_URL = 'static/'
MEDIA_URL = 'images/'


STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_ROOT = BASE_DIR / 'static/images'

STATIC_ROOT = BASE_DIR / "staticfiles"









# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL = 'static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
# MEDIA_URL = 'media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
