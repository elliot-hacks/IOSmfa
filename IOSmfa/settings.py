from pathlib import Path
import os
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/



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
    'mfa',
    'home',
    'fingerprint_api',
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

ROOT_URLCONF = 'IOSmfa.urls'

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

WSGI_APPLICATION = 'IOSmfa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DEBUG == True:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'django-insecure-9)0_+yc7_nmc&f999w6)fov8e30b9)qcj7r719+p+0*)7m^!0k'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['myDB'],
            'PORT': 3306,
            'HOST': 'localhost',
            'USER': os.environ['myUser'],
            'PASSWORD': os.environ['myPass'],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# MFA settings
MFA_UNALLOWED_METHODS=()   # Methods that shouldn't be allowed for the user
MFA_LOGIN_CALLBACK="accounts.views.login_user_in" # A function that should be called by username to login the user in session
MFA_RECHECK=True           # Allow random rechecking of the user
MFA_RECHECK_MIN=10         # Minimum interval in seconds
MFA_RECHECK_MAX=30         # Maximum in seconds
MFA_QUICKLOGIN=True        # Allows quick login for returning users

TOKEN_ISSUER_NAME="django_mfa2_example"      #TOTP Issuer name, this should be your project's name

if DEBUG:
  U2F_APPID="http://localhost"    #URL For U2F
  FIDO_SERVER_ID=u"localhost"      # Server rp id for FIDO2, it is the full domain of your project
else:
  U2F_APPID="https://django-mfa2-example.herokuapp.com"    #URL For U2F
  FIDO_SERVER_ID=u"django-mfa2-example.herokuapp.com"      # Server rp id for FIDO2, it is the full domain of your project

FIDO_SERVER_NAME=u"django_mfa2_example"
MFA_REDIRECT_AFTER_REGISTRATION = 'accounts:index'
MFA_SUCCESS_REGISTRATION_MSG = 'Your keys have successfully been created! You '
