"""
Django settings for ai_study_planner project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# SECURITY
# -------------------------------------------------------------------
# In production, load this from an environment variable, never hardcode it.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-CHANGE-THIS-KEY-BEFORE-DEPLOYMENT-xxxxxxxxxxxxx",
)

# Set DEBUG = False in production and configure ALLOWED_HOSTS properly.
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# -------------------------------------------------------------------
# APPLICATIONS
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "accounts",
    "core",
    "subjects",
    "tasks",
    "exams",
    "goals",
    "planner",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ai_study_planner.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom context processor: exposes sidebar/nav stats globally
                "core.context_processors.global_stats",
            ],
        },
    },
]

WSGI_APPLICATION = "ai_study_planner.wsgi.application"
ASGI_APPLICATION = "ai_study_planner.asgi.application"

# -------------------------------------------------------------------
# DATABASE (PostgreSQL)
# -------------------------------------------------------------------
# Configure these via environment variables in production.
# Create the DB first in pgAdmin / psql:
#   CREATE DATABASE ai_study_planner;
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_study_planner',
        'USER': 'postgres',
        'PASSWORD': 'Naveen@6381',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# -------------------------------------------------------------------
# CUSTOM USER MODEL
# -------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "core:dashboard"
LOGOUT_REDIRECT_URL = "core:home"

# -------------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # used by collectstatic in production

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------
# EMAIL (for password reset / reminders) - configure real SMTP in production
# -------------------------------------------------------------------
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "AI Study Planner <noreply@studyplanner.com>")

# -------------------------------------------------------------------
# MESSAGES FRAMEWORK
# -------------------------------------------------------------------
from django.contrib.messages import constants as messages_constants  # noqa: E402

MESSAGE_TAGS = {
    messages_constants.DEBUG: "secondary",
    messages_constants.INFO: "info",
    messages_constants.SUCCESS: "success",
    messages_constants.WARNING: "warning",
    messages_constants.ERROR: "danger",
}
