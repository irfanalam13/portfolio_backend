import os
from pathlib import Path
from decouple import config
import dj_database_url




DEBUG = config("DEBUG", default=False, cast=bool)


ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = config(
        "CORS_ALLOWED_ORIGINS",
        default="",
        cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
    )

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
)

CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
)

# =========================
# 🔐 SECURITY (PRODUCTION)
# =========================
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # force HTTPS

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ✅ BASE DIR (must be first)
BASE_DIR = Path(__file__).resolve().parent.parent



# 🔐 SECURITY
SECRET_KEY = config("SECRET_KEY", default="dev-secret-key")

# LOGGING = {
#     "version": 1,
#     "handlers": {
#         "console": {"class": "logging.StreamHandler"},
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "ERROR",
#     },
# }
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_yasg",

    # Local apps
    "apps.core",
    "apps.projects",
    "apps.blog",
    "apps.skills",
    "apps.problem_solver",
    "apps.contact",
    "apps.activity",
    "apps.ai",
]

# =====================================================
# ⚙️ MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 👈 MUST be here (top)

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 🌐 ROOT URL
ROOT_URLCONF = "config.urls"

# 🖼 TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # ✅ ADD THIS LINE
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ⚡ WSGI
WSGI_APPLICATION = "config.wsgi.application"

# 🗄 DATABASE (PostgreSQL)





ENV = config("ENV", default="development")

DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL", default=""),
        conn_max_age=600,
        ssl_require=(ENV == "production")
    )
}
# DATABASES = {
#     "default": dj_database_url.config(
#         default=os.environ.get("DATABASE_URL")
#     )
# }

# 🌍 AUTH (future SaaS ready)
AUTH_USER_MODEL = "auth.User"  # update later if custom



# 📁 MEDIA FILES
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ✅ STATIC FILES
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# 🧠 DRF CONFIG
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
    ],
}

# 🌍 TIMEZONE
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"