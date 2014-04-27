# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

SECRET_KEY = 'ne46)n1okvw*qt#0tt6qu^3ckfa_5ggsnds%=z7exeb(k-b*xi'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

DEFAULT_CHARSET='utf-8'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'imagekit',
    'userena',
    'guardian',
    'captcha',    
    'easy_thumbnails',
    'study_project.main',
    'study_project.lection_part',
    'study_project.practic_part',
    'study_project.accounts'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'userena.middleware.UserenaLocaleMiddleware'
)

SITE_ID = 1

AUTHENTICATION_BACKENDS = (  
        'userena.backends.UserenaAuthenticationBackend',  
        'guardian.backends.ObjectPermissionBackend',  
        'django.contrib.auth.backends.ModelBackend',  
    )  
  
ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'accounts.MyProfile'
  
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'  
LOGIN_URL = '/accounts/signin/'  
LOGOUT_URL = '/accounts/signout/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True  
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'makhstudyproject@gmail.com'  
EMAIL_HOST_PASSWORD = 'qweasd123zxc'  


ROOT_URLCONF = 'study_project.urls'

WSGI_APPLICATION = 'study_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'study_project_db',
        'USER': 'mk',
        'PASSWORD': '1',
        'HOST': '',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = ('d E Y')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


_PATH = os.path.abspath(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(_PATH, 'files', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(_PATH, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(_PATH, 'files','static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

ADMIN_MEDIA_PREFIX = '/static/admin/'
