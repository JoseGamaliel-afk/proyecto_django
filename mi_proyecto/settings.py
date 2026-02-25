from pathlib import Path
import os
import pymysql
pymysql.install_as_MySQLdb()

import cloudinary
import cloudinary.uploader
import cloudinary.api
import dj_database_url


# ======================
# BASE
# ======================
BASE_DIR = Path(__file__).resolve().parent.parent


# ======================
# SECURITY
# ======================
SECRET_KEY = 'django-insecure-1db3ex!7)3@@nq#xj766n(24!r)hhf7m)a4#s^h(k$1i%%spi4'
DEBUG = False
ALLOWED_HOSTS = ['*']


# ======================
# APPLICATIONS
# ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Paginas',
]


# ======================
# MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 👈 CLAVE PARA CSS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ======================
# URLS / WSGI
# ======================
ROOT_URLCONF = 'mi_proyecto.urls'

WSGI_APPLICATION = 'mi_proyecto.wsgi.application'


# ======================
# TEMPLATES
# ======================
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


# ======================
# DATABASE (PostgreSQL - Render)
# ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_n4t3',
        'USER': 'jose_afk',
        'PASSWORD': 'X6HhebykXWGArDF5nyP31gzgoQSCJQxk',
        'HOST': 'dpg-d6ffc214tr6s73bt51l0-a.oregon-postgres.render.com',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}


# ======================
# INTERNATIONALIZATION
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ======================
# STATIC FILES (CSS, JS, IMAGES)
# ======================
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'Paginas' / 'static'
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ======================
# DEFAULT PK
# ======================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ======================
# RECAPTCHA
# ======================
RECAPTCHA_SITE_KEY = '6Ld1JEosAAAAAH03XO1iLrjjXk0sIRlgt1uzxtY1'
RECAPTCHA_SECRET_KEY = '6Ld1JEosAAAAACzCDuudTQCeaG-ENgy97Rhv_LO-'


# ======================
# CLOUDINARY
# ======================
os.environ["CLOUDINARY_CLOUD_NAME"] = "dedxp9aoz"
os.environ["CLOUDINARY_API_KEY"] = "863341654834476"
os.environ["CLOUDINARY_API_SECRET"] = "1qWXamtfvA-jV8khHX-Msh_PVsg"

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)
