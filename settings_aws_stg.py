"""
Django settings for QED project when running with Docker.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import logging
import os
import socket
from settings import *
from temp_config.set_environment import DeployEnv
from django.utils.crypto import get_random_string

# Determine env vars to use:
runtime_env = DeployEnv()
runtime_env.load_deployment_environment()

print('settings_aws_stg.py')

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
SECRET_KEY = get_random_string(50, chars)
print(f"SECRET_KEY: {SECRET_KEY}")

GL_AWS = bool(os.getenv("GL_AWS", "0") == "1")
print(f"EPA-AWS: {GL_AWS}")
IN_PROD = bool(os.getenv("IN_PROD", "1") == "1") if not GL_AWS else True
print("Production Deployment: {}".format(IN_PROD))
if IN_PROD:
    DEBUG = False
    IS_PUBLIC = True
    CORS_ORIGIN_ALLOW_ALL = False
    PUBLIC_APPS = ['cts', 'hms', 'pisces', 'cyanweb']
    PASSWORD_REQUIRED = False
    os.environ.update({'HMS_RELEASE': 'True'})
else:
    DEBUG = True
    IS_PUBLIC = False
    CORS_ORIGIN_ALLOW_ALL = True
    PASSWORD_REQUIRED = True
    PUBLIC_APPS = ['cts', 'hms', 'pisces', 'cyan', 'pram']

# Get machine IP address
MACHINE_ID = socket.gethostname()

for key, val in os.environ.items():
    logging.info("QED DJANGO ENV VAR: {}: {}".format(key, val))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'REST_SERVER_8': 'http://172.20.100.18',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',  # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',
})

TEMPLATE_DEBUG = False

if not os.environ.get('UBERTOOL_REST_SERVER'):
    # Docker network
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://qed_nginx:7777'})
    print("REST backend = http://qed_nginx:7777")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
# try:
#     SECRET_KEY = os.getenv('DOCKER_SECRET_KEY', None)
#     if not SECRET_KEY:
#         with open('secrets/secret_key_django_dropbox.txt') as f:
#             SECRET_KEY = f.read().strip()
# except IOError as e:
#     print("Secret file not set as env variable or file")
#     down_low = 'Shhhhhhhhhhhhhhh'
#     SECRET_KEY = down_low

try:
    HOSTNAME = os.environ.get('DOCKER_HOSTNAME')
    #IS_PUBLIC = (os.environ.get('IS_PUBLIC') == "True")
    # with open('secret_key_django_dropbox.txt') as f:
    #        SECRET_KEY = f.read().strip()
except IOError as e:
    print("HOSTNAME address not set as env variable")
    HOSTNAME = 'unknown'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '*'
]

print("MACHINE_ID = {}".format(MACHINE_ID))
print("HOSTNAME = {}".format(HOSTNAME))
print("IS_PUBLIC = {}".format(IS_PUBLIC))

# Application definition
if IN_PROD:
    INSTALLED_APPS = (
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'cts_app',  # cts django app
        'cts_app.filters',  # cts filters for pchem table
        'cts_app.cts_api',
        'cts_app.cts_testing',
        'hms_app',  # hms django app
        'pisces_app',  # pisces django app
        'splash_app',  # splash django app
    )
else:
    INSTALLED_APPS = (
        'corsheaders',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'cts_app',  # cts django app
        'cts_app.filters',  # cts filters for pchem table
        'cts_app.cts_api',
        'cts_app.cts_testing',
        'cyan_app',  # cyan django app
        'hms_app',  # hms django app
        'hwbi_app',  # hwbi django app
        'nta_app',
        'pisces_app',  # pisces django app
        'pram_app',  # pram django app
        'splash_app',  # splash django app
    )


MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', #rollbar
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', #rollbar
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF=__name__, #rollbar

ROLLBAR = {
    'access_token': 'b626ac6c59744e5ba7ddd088a0075893',
    # 'environment': 'development', # if DEBUG else 'production',
    'environment': 'production',
    'branch': 'master',
    'root': '/var/www/qed',
}

ROLLBAR = {
    'access_token': 'POST_SERVER_ITEM_ACCESS_TOKEN',
    'environment': 'production',
    'branch': 'master',
    'root': os.getcwd()
}

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_docker.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Authentication
AUTH = False
# Note: env vars in os.environ always strings..
if PASSWORD_REQUIRED:
    logging.warning("Password protection enabled")
    MIDDLEWARE += [
        'login_middleware.RequireLoginMiddleware',
        'login_middleware.Http403Middleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
    AUTH = True
    # DEBUG = False

REQUIRE_LOGIN_PATH = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

secrets_path2 = os.path.join(KUBE_ROOT, 'data/django-secrets/secret_key_database.txt')
secrets_path1 = os.path.join(KUBE_ROOT, 'secrets/secret_key_database.txt')

if os.path.exists(secrets_path1):
    s_path = secrets_path1
else:
    s_path = secrets_path2
print(f"DB_PASS PATH: {s_path}")
try:
    with open(s_path) as f:
        DB_PASS = f.read().strip()
except IOError as e:
    print("{} not found!".format(s_path))
    DB_PASS = None

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    },
    'hem_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'hem_app/hem_db.sqlite3'),
    },
    'pisces_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PISCES_DB_NAME'),
        'USER': os.getenv('PISCES_DB_USER'),
        'PASSWORD': DB_PASS,
        'HOST': os.getenv('PISCES_DB_HOST'),
        'PORT': '5432',
    },
    'cyan_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'cyan_app/cyan_web_app_db.sqlite3')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC_ROOT = os.path.join('src', 'collected_static')
STATIC_ROOT = os.path.join('collected_static')
HMS_ANGULAR_APP_DIR = "/src/static_qed/hms/webapp"
HMS_ANGULAR_APP_ASSETS_DIR = "/src/static_qed/hms/webapp/assets"
CYANWEB_ANGULAR_APP_DIR = "/src/static_qed/epa-cyano-web"

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_qed'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_URL = '/static_qed/'
print(f"Staticfiles: {STATICFILES_DIRS}")

# Log to console in Debug mode
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
    )
