"""
Django settings for swe574 project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

import sys
import requests

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Include the apps folder in the path.
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: To keep the SECRET_KEY used in production secret, 
# the SECRET_KEY is retrieved from the environment variables.
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: DEBUG setting will be retrieved from the environment 
# variables to ensure that is not turned on during production.
# Environment variables come as a string, it is converted here to 
# integer first then a bool. Default value is 0.
DEBUG = bool(int(os.environ.get('DEBUG', 1)))

# ALLOWED_HOSTS is a security feature of Django to prevent HTTP Host 
# header attacks. The ALLOWED_HOSTS represent the host/domain names
# that the Django site can serve. The host names need to be specified 
# for production.
ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

if DEBUG == False:
    METADATA_URI = os.environ['ECS_CONTAINER_METADATA_URI']
    container_metadata = requests.get(METADATA_URI).json()
    ALLOWED_HOSTS.append(container_metadata['Networks'][0]['IPv4Addresses'][0])

# Environment variables come as a string. To retrieve ALLOWED_HOSTS
# environment variable, comma-separated list of different hostnames  
# are split and assigned to allowed hosts.
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get('ALLOWED_HOSTS', '').split(','),
    )
)

# Application definition

INSTALLED_APPS = [ 
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'coLearn',
    'chat',
    'quiz',
    'learning_space',
    'rest_framework',
    'storages',
    'tags'
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

ROOT_URLCONF = 'swe574.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], # Specifies the templates directory.
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

WSGI_APPLICATION = 'swe574.wsgi.application'
ASGI_APPLICATION = "swe574.asgi.application"

CHANNEL_LAYERS={
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

LOGIN_URL='/signin/'
LOGIN_REDIRECT_URL='/explore/'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# If Debug is set to true, the static files and media are served locally.
if DEBUG == True:
    STATIC_URL = '/static/static/'
    MEDIA_URL = '/static/media/'
    STATICFILES_DIRS=[os.path.join(BASE_DIR,"static")]

    MEDIA_ROOT = '/vol/web/media'
    STATIC_ROOT = '/vol/web/static'
    
# If debug is set to false, the static files are served from the S3 Bucket.
if DEBUG == False:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        BASE_DIR / "static"
    ]

    MEDIA_ROOT = BASE_DIR / "uploads"
    MEDIA_URL = '/files/'

    AWS_STORAGE_BUCKET_NAME = "swe574-group-1-static"
    AWS_S3_REGION_NAME = "eu-central-1"
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    STATICFILES_FOLDER = "static"
    MEDIAFILES_FOLDER = "media"

    STATICFILES_STORAGE = 'swe574.custom_storages.StaticFileStorage'
    DEFAULT_FILE_STORAGE = 'swe574.custom_storages.MediaFileStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
