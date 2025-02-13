from pathlib import Path
import os
from project_secrets.secrets_manager import SecretsManager
from django.core.cache import cache

# Base directories  ====================================================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Secrets ==============================================================================================================
if not SecretsManager.are_secrets_loaded():
    cache.clear()
    from project_secrets.entrypoint import EnvironmentLoader

    env_loader = EnvironmentLoader()
    env_loader.load()

# Environment-specific settings ========================================================================================
DEBUG = os.environ.get('DEBUG')

"""
1 - Development
0 - Staging / Production 
"""

if DEBUG == "0":
    ALLOWED_HOSTS = ['django']  # for nginx to refer to the django app in the docker-compose network
else:
    ...
    # ALLOWED_HOSTS = ['example.com'] # wherever django is installed

# Core Django settings ================================================================================================
SECRET_KEY = os.environ.get('SECRET_KEY')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth_app',
    'dashboard_app',
    'logger_app',
    'obtained_data_app',
    'user_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middlewares
    # 'project.middlewares.EstablishSessionMiddleware',
    'project.middlewares.NoCsrfForLocalhostMiddleware',  # TODO: Remove in production
    # 'project.middlewares.NonExistingPathsRedirectorMiddleware',
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

# Database settings ===================================================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'db.sqlite3',
    }
}

# Redis cache settings ================================================================================================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://redis:{os.environ.get("REDIS_EXTERNAL_PORT")}/1',
        'OPTIONS': {
            'PASSWORD': os.environ.get('REDIS_PASSWORD'),
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,
                'retry_on_timeout': True,
            },
        },
    },
}

# Nginx static files folder ============================================================================================
STATIC_ROOT = os.path.join(BASE_DIR, 'nginx', 'staticfiles')

# Password validation =================================================================================================
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

# Internationalization ================================================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Frontend stuff =======================================================================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static'),
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'frontend' / 'shared_templates',
            BASE_DIR / 'templates',
            ],
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

# Default primary key field type ======================================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
