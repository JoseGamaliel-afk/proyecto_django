from pathlib import Path
import pymysql
pymysql.install_as_MySQLdb()
import pymysql


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1db3ex!7)3@@nq#xj766n(24!r)hhf7m)a4#s^h(k$1i%%spi4'

DEBUG = False


ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Paginas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mi_proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mi_proyecto.wsgi.application'

import os
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse(
        'postgresql://jose_afk:OdkC2p4gJh46CkbzqoOt04LZrbWqNOeX@dpg-d5kgcnvpm1nc7383ghig-a.virginia-postgres.render.com/django_wkpc'
    )
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RECAPTCHA_SITE_KEY = '6Ld1JEosAAAAAH03XO1iLrjjXk0sIRlgt1uzxtY1'
RECAPTCHA_SECRET_KEY = '6Ld1JEosAAAAACzCDuudTQCeaG-ENgy97Rhv_LO-'

