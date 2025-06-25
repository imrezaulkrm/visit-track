from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*=(qt)sp7m4-jr-f7ils8-%#o$x$-jdh=bey2esl*7f#p3(cy('

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.123']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'visitors',         # তোমার visitors অ্যাপ
    'corsheaders',      # CORS support এর জন্য
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware - সবার উপরে রাখতে হয়
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Future এ template directory চাইলে এখানে path দিবে
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# PostgreSQL database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'visitor_db',         # তোমার ডাটাবেস নাম
        'USER': 'visitor',            # ডাটাবেস ইউজার
        'PASSWORD': 'visitor123',     # পাসওয়ার্ড
        'HOST': 'localhost',          # Docker হলে 'db'
        'PORT': '5432',
    }
}

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # DEV environment এর জন্য সব origin allow

# ⚠️ Future customization:
# যদি শুধু নির্দিষ্ট কিছু origin থেকে allow করতে চাও, নিচেরটা uncomment করো:
# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:5500",
#     "http://localhost:5173",
#     "http://192.168.1.123:5173",
# ]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
