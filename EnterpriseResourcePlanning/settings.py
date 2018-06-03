"""
Django settings for EnterpriseResourcePlanning project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'som=3zqd7=u7krx49fi%=$7gzzqs544=b#e2#+gh^$0w7*s(a*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Custom User Model
# AUTH_USER_MODEL = 'UserModel.User'

ALLOWED_HOSTS = ['*', '192.168.0.111', '192.168.43.155', '127.0.0.1', '172.20.10.3',
                 'akzarma.pythonanywhere.com', '10.42.0.1', '10.1.136.17', '192.168.0.15', '192.168.0.7',
                 '192.168.43.154']

DATA_UPLOAD_MAX_NUMBER_FIELDS = 5000

EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'noreply.viit@gmail.com'
EMAIL_HOST_PASSWORD = 'viitBublums'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'General.apps.GeneralConfig',
    'UserModel.apps.UsermodelConfig',
    'Exam.apps.ExamConfig',
    'Dashboard.apps.DashboardConfig',
    'Login.apps.LoginConfig',
    'Registration.apps.RegistrationConfig',
    'Timetable.apps.TimetableConfig',
    'Update.apps.UpdateConfig',
    'Requests.apps.RequestsConfig',
    'BackupRestore.apps.BackuprestoreConfig',
    'Attendance.apps.AttendanceConfig',
    'Research.apps.ResearchConfig',
    'Internship.apps.InternshipConfig',
    'Report.apps.ReportConfig',
    'django.contrib.humanize',
    'widget_tweaks',
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

ROOT_URLCONF = 'EnterpriseResourcePlanning.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'EnterpriseResourcePlanning.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR, '')
# session conf
minutes = 30
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = minutes * 60

APPEND_SLASH = True

NOTIFICATION_SMALL_LIMIT = 5
NOTIFICATION_LONG_LIMIT = 50

BROKER_URL = 'amqp://guest:**@localhost:5672//'

# APPEND_SLASH=True


# Tables to restore
# RESTORE = []


RESTORE_BATCH_SIZE = 500
