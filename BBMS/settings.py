from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import json

# 📦 Load environment variables
load_dotenv()

# ✅ Project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# 🔐 Security Settings
# -------------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("❌ DJANGO_SECRET_KEY is not set in environment variables.")

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# ✅ Use JSON-based ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ✅ CSRF trusted origins
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "https://bloodbank-backend-zvbu.onrender.com"
).split(",")

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
X_FRAME_OPTIONS = 'DENY'

PORT = os.environ.get("PORT", "8000")

# -------------------------------
# 📦 Installed Apps
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'blood',
    'axes',
    'accounts',
    'captcha',
    'widget_tweaks',
]

# -------------------------------
# ⚙️ Middleware
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    'axes.middleware.AxesMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------
# 🔐 Authentication Backends
# -------------------------------
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# -------------------------------
# 🔗 URL & Templates
# -------------------------------
ROOT_URLCONF = 'BBMS.urls'

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

WSGI_APPLICATION = 'BBMS.wsgi.application'

# -------------------------------
# 🗃️ Database (PostgreSQL on Render)
# -------------------------------
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=not DEBUG
    )
}

# -------------------------------
# 🔐 Password Validators
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# 🌍 Internationalization
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------
# 🎨 Static Files
# -------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# -------------------------------
# 🔑 Default Primary Key
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# 🔐 Session & Login Behavior
# -------------------------------
LOGIN_URL = 'login'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_REDIRECT_URL = '/accounts/dashboard/'

# -------------------------------
# 🛡️ Django Axes Configuration
# -------------------------------
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCKOUT_CALLABLE = 'blood.views.custom_lockout_response'
AXES_ENABLED = True

# ✅ Force CSRF and session cookies to be secure (for HTTPS on Render)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True