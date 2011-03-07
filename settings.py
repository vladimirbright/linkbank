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
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
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
ADMIN_MEDIA_PREFIX = '/media/'


LOGIN_URL = '/signin/'

TEMPLATE_DIRS = (
    self_dir('templates'),
)

DEV_MEDIA_URL = '/devs/'
PRODUCTION_MEDIA_URL = '/st/'
ROOT_MEDIA_FILTERS = {
    'css': 'mediagenerator.filters.yuicompressor.YUICompressor',
    'js': 'mediagenerator.filters.closure.Closure',
}
CLOSURE_COMPILER_PATH = self_dir("compiler.jar")
YUICOMPRESSOR_PATH = self_dir("yuicompressor-2.4.2.jar")

GLOBAL_MEDIA_DIRS = (
    self_dir('s'),
)

MEDIA_BUNDLES = (
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
    ('main.js',
        'js/mootools-core-1.3-full-compat.js',
        'js/mootools-more.js',
        'js/clientcide.2.2.0.js',
    ),
    ('my.js',
        'js/placeholder.moo.js',
        'js/bookmarks.moo.js',
        'js/navigation.moo.js',
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
# Sphinx
SPHINXS = {
    "default": ( "127.0.0.1", 9312 ),
}

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
    'django.contrib.webdesign',
    'gravatar',
    'helpers',
    'mediagenerator',
    'pagination',
    'south',
    'tags',
)


try:
    from local_settings import *
except ImportError:
    pass

MEDIA_DEV_MODE = DEBUG

