import os
from pathlib import Path
from datetime import timedelta
import dj_database_url
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD: En prod usar variables, hoy hardcodeamos para la demo
load_dotenv() # Carga las variables del .env

# Y más abajo, cambia las variables quemadas por estas:
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'# Importante: False simula producció / pasara true cuando se esta utilizando dentro de el local


# 1. PERMITIR A RENDER
ALLOWED_HOSTS = ['reservalab-api.onrender.com', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt', # 1. JWT (Autenticación)
    'rest_framework',
    'corsheaders', # 2. CORS (Angular)

    # Mis Apps de ReservaLab
    'accounts',
    'labs',
    'equipment',
    'reservations',
    'loans',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # 3. Whitenoise (Estáticos)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # 4. CORS Middleware (Antes de Common)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 5. CONFIGURACIÓN CORS (Permitir todo por hoy)
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Base de datos (SQLite por hoy para no fallar en la demo)
import os

if os.getenv('DATABASE_URL'):
    # 👇 CONFIGURACIÓN PARA PRODUCCIÓN (RENDER + SUPABASE)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres', # Por defecto en Supabase es postgres
            'USER': 'postgres', # Por defecto en Supabase es postgres
            'PASSWORD': 'MU&X32unFj2.y/@', # <-- Pon tu contraseña limpia aquí
            'HOST': 'db.shrzucphsaieewkgjahd.supabase.co', # <-- Copia el Host que te da Supabase
            'PORT': '5432', # El puerto pooler de Supabase suele ser 6543 o 5432
        }
    }
else:
    # 👇 CONFIGURACIÓN PARA DESARROLLO LOCAL (TU COMPUTADORA)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [] 

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# 6. ARCHIVOS ESTÁTICOS (Whitenoise)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.Usuario'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}