from .base import *



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2f6ea6i)y+yrq3bw83)^y#0$ljnjk$5x)l2-9tlgmy5sloh!y*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_ROOT = BASE_DIR / 'staticfiles'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nonso.udonne@gmail.com'
EMAIL_HOST_PASSWORD = 'nonso-1406'
# config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
