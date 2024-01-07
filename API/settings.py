"""
Django settings for API project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jntx)acjxyah^40fg5(!rdnp3c*1f6$)v&64u32-(a3suwh%@t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.postgres',

    'corsheaders',

    'rest_framework',
    'rest_framework.authtoken',
    'encryption',
    'django_filters',

    'drf_yasg'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]

}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 'encryption.access_middleware.AccessMiddleware'
]

AUTH_USER_MODEL = 'encryption.EncryptionUser'

ROOT_URLCONF = 'API.urls'

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

WSGI_APPLICATION = 'API.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db2',
        'PORT': 5432
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

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# STATIC_ROOT = BASE_DIR / "encryption/static"

# MEDIA_URL = 'http://localhost:9000/api-data/'
# MEDIA_ROOT = BASE_DIR / "encryption/media"


# Старый конфиг
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_FILE_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'api-data'     # Бакет должен уже быть создан
AWS_ACCESS_KEY_ID = os.environ.get('MINIO_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.environ.get('MINIO_SECRET_KEY')
AWS_S3_ENDPOINT_URL = os.environ.get('MINIO_HOST')
#
# STATIC_URL = 'http://localhost:9000/' + AWS_STORAGE_BUCKET_NAME + '/'

# #Новый конфиг
# MINIO_ROOT_USER = os.environ.get('MINIO_ACCESS_KEY')
# MINIO_ROOT_PASSWORD = os.environ.get('MINIO_SECRET_KEY')
# MINIO_STORAGE_ENDPOINT = os.environ.get('MINIO_HOST', 'http://nginx:9000')
# # MINIO_STORAGE_MEDIA_BUCKET_NAME = os.environ.get('MINIO_STORAGE_MEDIA_BUCKET_NAME', 'your-media-bucket-name')
# # MINIO_STORAGE_STATIC_BUCKET_NAME = os.environ.get('MINIO_STORAGE_STATIC_BUCKET_NAME', 'your-static-bucket-name')
# MINIO_STORAGE_STATIC_BUCKET_NAME = 'api-data'
#
# # Используйте минио как хранилище для статики
# STATIC_URL = MINIO_STORAGE_ENDPOINT + '/' + MINIO_STORAGE_STATIC_BUCKET_NAME + '/'
# STATICFILES_STORAGE = 'minio_storage.storage.MinioStaticStorage'

# Используйте минио как хранилище для медиафайлов
# DEFAULT_FILE_STORAGE = 'minio_storage.storage.MinioMediaStorage'
# MEDIA_URL = MINIO_STORAGE_ENDPOINT + '/' + MINIO_STORAGE_MEDIA_BUCKET_NAME + '/'

TIME_ZONE = 'Europe/Moscow'

# CSRF_TRUSTED_ORIGINS = [
#     'https://nginx'
# ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://mikhailvolvach.github.io"
    # Добавьте здесь другие разрешенные источники, если необходимо
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
