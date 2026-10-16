import os
from pathlib import Path
from decouple import config
import dj_database_url
import cloudinary

cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET"),
)

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

OPENAI_API_KEY = config("OPENAI_API_KEY", default=None)

# GitHub username for the public activity feed (empty disables the call).
GITHUB_USERNAME = config("GITHUB_USERNAME", default="")

DEBUG = config("DEBUG", default=False, cast=bool)


ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    "https://portfolio-backend-srq8.onrender.com",
    "https://www.irfanalam.com.np",
    "https://irfanalam.com.np",
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:3000,https://irfanalam.com.np,https://www.irfanalam.com.np",
    cast=lambda v: [s.strip() for s in v.split(",") if s.strip()],
)

# CSRF_TRUSTED_ORIGINS = config(
#     "CSRF_TRUSTED_ORIGINS",
#     default="",
#     cast=lambda v: [s.strip() for s in v.split(",") if s.strip()]
# )



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

# Never ship the insecure dev key to production.
if not DEBUG and SECRET_KEY == "dev-secret-key":
    raise RuntimeError("SECRET_KEY must be set via environment in production.")

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
    "cloudinary",
    "cloudinary_storage",

    # Local apps
    "apps.core",
    "apps.projects",
    "apps.blog",
    "apps.skills",
    "apps.problem_solver",
    "apps.contact",
    "apps.activity",
    "apps.ai",
    "apps.achievements",
    "apps.education",
    "apps.experience",
    "apps.timeline",


]

# =====================================================
# ⚙️ MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",  # compress API/JSON + HTML responses
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

DATABASE_URL = config("DATABASE_URL", default=None)

if not DATABASE_URL:
    raise Exception("❌ DATABASE_URL is not set")

DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=(ENV == "production"),
    )
}
# DATABASES = {
#     "default": dj_database_url.config(
#         default=os.environ.get("DATABASE_URL")
#     )
# }

# 🌍 AUTH (future SaaS ready)
AUTH_USER_MODEL = "auth.User"  # update later if custom


# ================================
# ☁️ MEDIA FILES (Cloudinary)
# ================================



# ✅ STATIC FILES
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

STATIC_ROOT = BASE_DIR / "staticfiles"



# 🧠 DRF CONFIG
#
# NOTE: no global default throttle classes. Read endpoints are server-rendered
# (all SSR requests share the Next.js server IP), so a global AnonRateThrottle
# would throttle every visitor at once. Instead we apply ScopedRateThrottle only
# to the write endpoints that are called directly from the browser (real client
# IPs): the contact form and the AI assistant.
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_RATES": {
        "contact": "5/hour",
        "ai": "15/hour",
    },
}

# 🗃 CACHE (local-memory; swap BACKEND/LOCATION for Redis later via env var)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "portfolio-cache",
    }
}

# 🌍 TIMEZONE
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"