"""
Django settings for appMain project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from dotenv import dotenv_values

#importa las variables de .env
config = dotenv_values(".env")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^l^5d#^x*tfuc-#pl^b+9ul9x(ju(&x_b4jk+&ew&r*3j_v!g2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['conbcoerp.com', '18.223.167.9', '127.0.0.1', 'www.cbr.com', 'cbr.com', '190.92.148.128', "azenv.net"]

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'CBR'
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

ROOT_URLCONF = 'appMain.urls'

#DEFAULT_FILE_STORAGE = 'db_file_storage.storage.DatabaseFileStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'appMain.wsgi.application'

try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'contag2',
            'USER': config['USUARIO_POSTGRES'],
            'PASSWORD': config['PASSWORD_POSTGRES'],
            'HOST': 'localhost',
            'PORT': '5432',
        }
    
    }
except:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'contag2',
            'USER': "pestevez",
            'PASSWORD': "pestevez123",
            'HOST': 'localhost',
            'PORT': '5432',
        }
    
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Lima'
USE_I18N = True

USE_L10N = True

USE_TZ = True


FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_TEMP_DIR = '/tmp'



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticdef')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')   
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')