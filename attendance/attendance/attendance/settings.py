from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-otjf2loo30qo7(86lhs8h5%#pn-$kp5y0!ai13buetoxbg6x2g'

DEBUG = True

# -----------------------------
# HOSTS
# -----------------------------
ALLOWED_HOSTS = ["*"]


# -----------------------------
# INSTALLED APPS
# -----------------------------
INSTALLED_APPS = [
    'corsheaders',   # 🔥 MUST BE FIRST

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'attendance_app',
    'storages',
]


# -----------------------------
# MIDDLEWARE (ORDER IMPORTANT)
# -----------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 🔥 MUST BE FIRST

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# -----------------------------
# 🔥 CORS CONFIG (FIXED)
# -----------------------------

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://provision-attendance.prowesstics.co.in",

    # ✅ ADD YOUR NGROK URL HERE (VERY IMPORTANT)
    "https://8fe7-49-204-125-104.ngrok-free.app",
]

# 🔥 IMPORTANT FOR NGROK (dynamic URLs)
CORS_ALLOW_ALL_ORIGIN_REGEXES = [
    r"https://.*\.ngrok-free\.app",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "ngrok-skip-browser-warning",
]


# -----------------------------
# 🔥 CSRF FIX (IMPORTANT)
# -----------------------------
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://provision-attendance.prowesstics.co.in",

    # ✅ ADD NGROK HERE ALSO
    "https://8fe7-49-204-125-104.ngrok-free.app",
]

# -----------------------------
# MEDIA
# -----------------------------
# MEDIA_URL = '/media/'
# MEDIA_ROOT = r'D:\Vision Analytics\Face_recog\evidence_images'



DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_ACCOUNT_NAME = 'provisions'
AZURE_ACCOUNT_KEY = '5iJJ/k1ojQg1D3irjN65h5dfJIbjid5kLcdjbf4Gtd5e2XbZZenJTb1MxXCkOxTe7xS6MCUqk5O3+AStNF8G9g=='
AZURE_CONTAINER = 'media'

MEDIA_URL = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER}/"


# -----------------------------
# EMAIL
# -----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'manikandan.m@prowesstics.com'
EMAIL_HOST_PASSWORD = 'xble reyp dotl cnfg'


# -----------------------------
# ROOT URL
# -----------------------------
ROOT_URLCONF = 'attendance.urls'


# -----------------------------
# TEMPLATES
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


WSGI_APPLICATION = 'attendance.wsgi.application'


# -----------------------------
# DATABASE
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Attendance_tracking',
        'USER': 'postgres',
        'PASSWORD': 'pro@123',
        'HOST': '64.227.171.26',
        'PORT': '5432',
    }
}


# -----------------------------
# TIMEZONE
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True

# -----------------------------
# STATIC
# -----------------------------
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
