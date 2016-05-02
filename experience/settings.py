from __future__ import absolute_import
"""
Django settings for experience project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import djcelery

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-12agj@o!r$2yg^a_#o)r82zhz!lsi3w3%@hrg-bqzna3a=tp9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['python-guilherme.com.br', 'ec2-54-149-230-4.us-west-2.compute.amazonaws.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'geolocation',
    'twitterbot',
    'oportunidades',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'experience.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['experience/templates'],
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

WSGI_APPLICATION = 'experience.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'experience',
        # 'USER': 'postgres',
        # 'PASSWORD': 'postgres',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CONSUMER_KEY = 'OQ5SVO2hFysxDQs3yPKPtgvTY'
CONSUMER_SECRET = 'JXYsMjFEmC909HFff4o4XU3EYPJc2hNl68VGE87L4E4J0xsxoQ'
ACCESS_TOKEN_KEY = '2389356595-poRfonUKQtV8Nt60r4FsAG81LjyKzGmj5igaXcS'
ACCESS_TOKEN_SECRET = 'Pz5xo6ku4dk7xZtdL2DWDldTsbzbtOnxiKjWjhtzRrlVN'


# CELERY SETTINGS
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERYD_CONCURRENCY=10
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_ERROR_EMAILS = True

djcelery.setup_loader()

# hack for djcelery migration issue
from django.db import connection
if 'djcelery_taskstate' in connection.introspection.table_names():
    # if djcelery is already in database ignore migrations
    MIGRATION_MODULES = {'djcelery': None,}

try:
    from settings_local import *
except ImportError:
    pass


from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    # Executes every 12 hours
    'add-every-12-hours': {
        'task': 'tasks.retweet',
        'schedule': crontab(minute=0, hour='*/12'),
    },
    # Executes every 3 days
    'add-every-3-days': {
        'task': 'tasks.retweet',
        'schedule': crontab(minute=0, hour=0, day_of_month='*/3'),
    },
}