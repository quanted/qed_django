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
from temp_config.set_environment import DeployEnv


print('settings_aws_stg.py')

ENV_CHECK = bool(os.getenv("ENV_NAME", "") == "kube_dev")
if not ENV_CHECK:
    print("Running deployment env setup from settings_aws_stg.py")
    runtime_env = DeployEnv()
    runtime_env.load_deployment_environment()

IN_PROD = bool(os.getenv("IN_PROD") == "1")
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

# Get local machine IP
def get_machine_ip():
    try:
        _MACHINE_ID = socket.gethostname()
        _MACHINE_INFO = socket.gethostbyname_ex(_MACHINE_ID)
        print("Development machine INFO: {}".format(_MACHINE_INFO))
    except:
        print("Unable to get machine IP")
        return None
    _MACHINE_IP = ""
    for ip in _MACHINE_INFO[2]:
        if '192' in ip:
            _MACHINE_IP = ip
    return _MACHINE_IP


MACHINE_IP = get_machine_ip()

KUBE_ROOT = os.path.abspath(os.path.dirname(__file__)).replace("qed_django", "")
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.join(KUBE_ROOT, 'templates_qed/')  # .replace('\\','/'))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'REST_SERVER_8': 'http://172.20.100.18',
    'PROJECT_PATH': PROJECT_ROOT,
    'SITE_SKIN': 'EPA',  # Leave empty ('') for default skin, 'EPA' for EPA skin
    'CONTACT_URL': 'https://www.epa.gov/research/forms/contact-us-about-epa-research',
})

TEMPLATE_DEBUG = False

if not os.environ.get('UBERTOOL_REST_SERVER'):
    os.environ.update({'UBERTOOL_REST_SERVER': 'http://qed_nginx:7777'})
    print("REST backend = http://qed_nginx:7777")

d_secret1 = os.path.join(KUBE_ROOT, 'data/django-secrets/secret_key_django_dropbox.txt')
d_secret2 = os.path.join(KUBE_ROOT, 'secrets/secret_key_django_dropbox.txt')
if os.path.exists(d_secret2):
    d_path = d_secret2
else:
    d_path = d_secret1
try:
    with open(d_path) as f:
        SECRET_KEY = f.read().strip()
except IOError as e:
    print("Could not find secret file: {}".format(d_path))
    down_low = 'Shhhhhhhhhhhhhhh'
    SECRET_KEY = down_low

if SECRET_KEY == "" or SECRET_KEY is None:
    SECRET_KEY = os.getenv('SECRET_KEY', "needtosetthesecretkey")

HOSTNAME = os.environ.get('DOCKER_HOSTNAME')

ALLOWED_HOSTS = []

if IN_PROD:
    ALLOWED_HOSTS.append('134.67.114.3')  # CGI NAT address (mapped to 'qed.epa.gov')
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('134.67.114.5')
    ALLOWED_HOSTS.append('172.20.100.11')
    ALLOWED_HOSTS.append('172.20.100.13')
    ALLOWED_HOSTS.append('172.20.100.15')
    ALLOWED_HOSTS.append('qed.epa.gov')
    ALLOWED_HOSTS.append('qed.edap-cluster.com')
    ALLOWED_HOSTS.append('ceamdev.ddns.net')
    ALLOWED_HOSTS.append('ceamstg.ddns.net')
    ALLOWED_HOSTS.append('ceamdev.ceeopdev.net')
    ALLOWED_HOSTS.append('ceamstg.ceeopdev.net')
    ALLOWED_HOSTS.append('qedlinux1dev.aws.epa.gov')
    ALLOWED_HOSTS.append('qedlinux1stg.aws.epa.gov')
    ALLOWED_HOSTS.append('awqedlinprd.aws.epa.gov')
elif HOSTNAME == "UberTool-Dev":
    ALLOWED_HOSTS.append('172.16.0.4')
    ALLOWED_HOSTS.append('qed.epacdx.net')
else:
    ALLOWED_HOSTS.append('localhost')
    ALLOWED_HOSTS.append('127.0.0.1')
    ALLOWED_HOSTS.append('host.docker.internal')
    ALLOWED_HOSTS.append('192.168.99.100')  # Docker Machine IP (generally, when using VirtualBox VM)
    ALLOWED_HOSTS.append('134.67.114.3')  # CGI NAT address (mapped to 'qed.epa.gov')
    ALLOWED_HOSTS.append('134.67.114.1')
    ALLOWED_HOSTS.append('134.67.114.5')
    ALLOWED_HOSTS.append('172.20.100.11')
    ALLOWED_HOSTS.append('172.20.100.13')
    ALLOWED_HOSTS.append('172.20.100.15')
    ALLOWED_HOSTS.append('qedinternal.epa.gov')
    ALLOWED_HOSTS.append('qed.epa.gov')
    ALLOWED_HOSTS.append('qedinternalblue.edap-cluster.com')
    ALLOWED_HOSTS.append('qedinternal.edap-cluster.com')
    ALLOWED_HOSTS.append('qed.edap-cluster.com')
    ALLOWED_HOSTS.append('qedblue.edap-cluster.com')
    ALLOWED_HOSTS.append('ceamdev.ddns.net')
    ALLOWED_HOSTS.append('ceamstg.ddns.net')
    ALLOWED_HOSTS.append('ceamdev.ceeopdev.net')
    ALLOWED_HOSTS.append('ceamstg.ceeopdev.net')
    ALLOWED_HOSTS.append('qedlinux1dev.aws.epa.gov')
    ALLOWED_HOSTS.append('qedlinux1stg.aws.epa.gov')
    ALLOWED_HOSTS.append('awqedlinprd.aws.epa.gov')

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

ROOT_URLCONF = __name__

WSGI_APPLICATION = 'wsgi_docker.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Authentication
AUTH = False
# Note: env vars in os.environ always strings..
if PASSWORD_REQUIRED:
    logging.warning("Password protection enabled")
    MIDDLEWARE_CLASSES += [
        'login_middleware.RequireLoginMiddleware',
        'login_middleware.Http403Middleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ]
    AUTH = True

REQUIRE_LOGIN_PATH = '/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join('collected_static')
HMS_ANGULAR_APP_DIR = "/src/static_qed/hms/webapp"
HMS_ANGULAR_APP_ASSETS_DIR = "/src/static_qed/hms/webapp/assets"
CYANWEB_ANGULAR_APP_DIR = "/src/static_qed/epa-cyano-web"

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_qed'),
)
print(f"Staticfiles: {STATICFILES_DIRS}")

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_URL = '/static_qed/'

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

