# -*- coding: utf-8 -*-

import os.path

SELF_DIR = os.path.abspath(os.path.dirname(__file__))

def self_dir(*args):
    return os.path.join(SELF_DIR, *args)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Vladimir', 'vladimirbright@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bookmarks',                      # Or path to database file if using sqlite3.
        'USER': 'bookmarks',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'
# LANGUAGE_CODE = 'ru-RU'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True

SECRET_KEY = '8_#0m81g!r@+dz@kqxl))4(w36bigo+jae#qqlh(w=n@znl0-a'

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "helpers.context_processors.current_site",
]

if DEBUG:
    TEMPLATE_CONTEXT_PROCESSORS.append("django.core.context_processors.debug")

THUMBNAIL_MEDIA_ROOT = self_dir('s/thumbs')
THUMBNAIL_MEDIA_URL = '/s/thumbs/'
MEDIA_ROOT = self_dir('s')
MEDIA_URL = '/s/'
STATIC_ROOT = self_dir('static')
STATIC_URL = '/static/'
AUTH_PROFILE_MODULE = 'bank.Profile'
LOGIN_URL = '/signin/'
TEMPLATE_DIRS = (
    self_dir('templates'),
)
DEV_MEDIA_URL = '/devs/'
PRODUCTION_MEDIA_URL = '/st/'
ROOT_MEDIA_FILTERS = {
    #'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.closure.Closure',
}
CLOSURE_COMPILER_PATH = self_dir("compiler.jar")
YUICOMPRESSOR_PATH = self_dir("yuicompressor-2.4.2.jar")
GLOBAL_MEDIA_DIRS = (
    self_dir('s'),
)
MEDIA_BUNDLES = (
    ("screen.bundle.css",
        "css/screen.css",
    ),
    ("ie.bundle.css",
        "css/ie.css",
    ),
    ("print.bundle.css",
        "css/ie.css",
    ),
    ("site.js",
        "js/Mootools.ClientSide.js",
        "js/Custom.Classes.js",
    ),
    ("login_or_register.css",
        'css/login_or_register.sass',
        'css/messages.sass',
        'css/forms.sass',
    ),
    ('main.css',
        'css/style.sass',
        'css/messages.sass',
        'css/forms.sass',
        'css/popup.sass',
    ),
)
LOCALE_DIRS = (
    self_dir('locale'),
)
ROOT_URLCONF = 'urls'
SOUTH_TESTS_MIGRATE = False
# Captcha
CAPTCHA_FONT_SIZE = 30;
CAPTCHA_FONT_PATH = self_dir('Ubuntu-R.ttf')
DJAPIAN_DATABASE_PATH = self_dir('djapian_spaces')
INSTALLED_APPS = (
    'bank',
    'captcha',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'gravatar',
    'helpers',
    'mediagenerator',
    'pagination',
    'south',
)

ALLOWED_HOSTS = ('knbase.info', 'linkbank.dev')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}


try:
    from local_settings import *
except ImportError:
    pass

MEDIA_DEV_MODE = DEBUG

