"""
Django settings for sh8email project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

#####################################################

If you want to sh8email application with this production settings,
set OS environment variable "DJANGO_SETTINGS_MODULE" to 'sh8email.settings_prod',
using below command.
$ export DJANGO_SETTINGS_MODULE=sh8email.settings_prod
    - by Wonyoung Ju
"""
from .settings import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SH8EMAIL_DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sh8email',
        'USER': 'sh8email',
        'PASSWORD': os.environ['SH8EMAIL_POSTGRES_PW'],
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}


# Mail receiving server settings
MAIL_SERVER_PORT = 25

# Logging
# https://docs.djangoproject.com/en/1.8/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'with_time': {
            'format': '[%(levelname)s] [%(asctime)s] [Logger: %(name)s]\n%(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'console_error': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'with_time',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'slack_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django_slack.log.SlackExceptionHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'console_error', 'slack_admins'],
        },
        'django.request': {
            'handlers': ['console', 'console_error', 'slack_admins'],
            'level': 'ERROR',
            'propagate': False
        },
        'django.security': {
            'handlers': ['console', 'console_error', 'slack_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# django-slack
# https://django-slack.readthedocs.io/
SLACK_TOKEN = os.environ['SH8EMAIL_SLACK_TOKEN']
SLACK_CHANNEL = '#sh8email-server'

# Backdoor
BACKDOOR_KEY = os.environ['SH8EMAIL_BACKDOOR_KEY']
