import os
from pathlib import Path
import environ  


BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=True)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DB_NAME", ),  
        'USER': env("DB_USER", ),  
        'PASSWORD': env("DB_PASSWORD",),  
        'HOST': env("DB_HOST", ),  
        'PORT': env("DB_PORT"),  
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',  
    'chat', 
]


ASGI_APPLICATION = "chatbot_project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'chatbot_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"], 
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

WSGI_APPLICATION = 'chatbot_project.wsgi.application' 


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",  
]

STATIC_ROOT = BASE_DIR / "staticfiles"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = "django.contrib.sessions.backends.cache"  
SESSION_CACHE_ALIAS = "default"  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  
SESSION_COOKIE_AGE = 100  
APPEND_SLASH = False

