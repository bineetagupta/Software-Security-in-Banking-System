"""
Django settings for group3_sbs project.

Generated by 'django-admin startproject' using Django 1.10.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm54o^3a8-&f45s(fvwa6_9-m8e5i)!#70)@t2*cbx=x12jl3di'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'global_templates',
    'internal',
    'external',
    'reset',
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

ROOT_URLCONF = 'group3_sbs.urls'

# Logging settings
# https://docs.djangoproject.com/en/1.10/topics/logging/
# https://github.com/jgutbub/CSE_545/wiki/Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './log/server_log.log',
        },
        'login_handler': {
            'class': 'logging.FileHandler',
            'filename': './log/login_log.log',
        },
        'internal_handler': {
            'class': 'logging.FileHandler',
            'filename': './log/internal_log.log',
        },
        'external_handler': {
            'class': 'logging.FileHandler',
            'filename': './log/external_log.log',
        },
        'global_templates_handler': {
            'class': 'logging.FileHandler',
            'filename': './log/global_templates_log.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'login': {
            'handlers': ['login_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'internal': {
            'handlers': ['internal_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'external': {
            'handlers': ['external_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'global_templates': {
            'handlers': ['global_templates_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'group3_sbs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'group3_sbs',
        'USER': 'root',
        'PASSWORD': 'cse545',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Arizona'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Session settings
# https://docs.djangoproject.com/en/1.10/topics/http/sessions/

# 10 minute session life
SESSION_COOKIE_AGE = 600

# Delete session once browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Update the session life upon each request
SESSION_SAVE_EVERY_REQUEST = True


# Email Setup
# https://docs.djangoproject.com/en/1.10/topics/email/
# https://github.com/jgutbub/CSE_545/wiki/Sending-mail

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'group3sbs@gmail.com'
EMAIL_HOST_PASSWORD = 'asussgroup3'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django.TemplateBackend'

# Login
LOGIN_URL = "/login/"
