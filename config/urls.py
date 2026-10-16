
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.urls import include, path, re_path
from django.utils import timezone

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


# --------------------------------------------------
# API Documentation
# --------------------------------------------------

schema_view = get_schema_view(
    openapi.Info(
        title="Irfan Alam Portfolio API",
        default_version="v1",
        description=(
            "REST API powering the Irfan Alam portfolio. "
            "Provides projects, blogs, skills, education, "
            "experience, achievements, contact, and more."
        ),
        contact=openapi.Contact(
            email="contact.dev.irfan@gmail.com"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# --------------------------------------------------
# API Root
# --------------------------------------------------

def api_root(request):
    """Return API information and available endpoints."""

    return JsonResponse({
        "name": "Irfan Alam Portfolio API",
        "status": "operational",
        "message": "Welcome to the portfolio API.",
        "version": "v1",
        "timestamp": timezone.now().isoformat(),
        "documentation": {
            "swagger": request.build_absolute_uri("swagger/"),
            "redoc": request.build_absolute_uri("redoc/"),
        },
        "endpoints": {
            "core": "/api/core/",
            "projects": "/api/projects/",
            "blogs": "/api/blogs/",
            "skills": "/api/skills/",
            "problem_solving": "/api/problem_solving/",
            "contacts": "/api/contacts/",
            "activity": "/api/activity/",
            "ai": "/api/ai/",
            "education": "/api/education/",
            "experience": "/api/",
            "timeline": "/api/timeline/",
        },
        "health": "/health/",
    })


# --------------------------------------------------
# Health Check
# --------------------------------------------------

def health_check(request):
    """Basic application health check."""

    return JsonResponse({
        "status": "healthy",
        "service": "portfolio-api",
        "timestamp": timezone.now().isoformat(),
    })


# --------------------------------------------------
# Error Handlers
# --------------------------------------------------

def custom_404_view(request, exception):
    return JsonResponse(
        {
            "status": "error",
            "code": 404,
            "message": "The requested resource was not found.",
            "path": request.path,
        },
        status=404,
    )


def custom_500_view(request):
    return JsonResponse(
        {
            "status": "error",
            "code": 500,
            "message": "An unexpected server error occurred.",
        },
        status=500,
    )


handler404 = "config.urls.custom_404_view"
handler500 = "config.urls.custom_500_view"


# --------------------------------------------------
# URL Patterns
# --------------------------------------------------

urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health_check, name="health-check"),

    path("admin/", admin.site.urls),

    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),

    path("api/core/", include("apps.core.urls")),
    path("api/projects/", include("apps.projects.urls")),
    path("api/blogs/", include("apps.blog.urls")),
    path("api/skills/", include("apps.skills.urls")),
    path(
        "api/problem_solving/",
        include("apps.problem_solver.urls"),
    ),
    path("api/contacts/", include("apps.contact.urls")),
    path("api/activity/", include("apps.activity.urls")),
    path("api/ai/", include("apps.ai.urls")),
    path("api/education/", include("apps.education.urls")),
    path("api/experience/", include("apps.experience.urls")),
    path("api/", include("apps.achievements.urls")),
    path("api/timeline/", include("apps.timeline.urls")),
]


# Serve uploaded media locally only during development.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )







# from django.urls import path, include, re_path

# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static

# from django.http import JsonResponse

# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="My API",
#         default_version='v1',
#         description="API documentation",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )







# def custom_404_view(request, exception):
#     return JsonResponse(
#         {"error": "Not found"},
#         status=404
#     )


# def custom_500_view(request):
#     return JsonResponse(
#         {
#             "error": "Server error",
#             "debug": str(request) if settings.DEBUG else None
#         },
#         status=500
#     )


# handler404 = "config.urls.custom_404_view"
# handler500 = "config.urls.custom_500_view"


# urlpatterns = [
#     # Admin panel
#     path("admin/", admin.site.urls),
#     re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
#     re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0)),

#     path("api/core/", include("apps.core.urls")),

#     path("api/projects/", include("apps.projects.urls")),
#     path("api/blogs/", include("apps.blog.urls")),
#     path("api/skills/", include("apps.skills.urls")),
#     path("api/problem_solving/", include("apps.problem_solver.urls")),  # problems + solutions
#     path("api/contacts/", include("apps.contact.urls")),
#     path("api/activity/", include("apps.activity.urls")),
#     path("api/ai/", include("apps.ai.urls")),
#     path("api/education/", include("apps.education.urls")),
#     path("api/experience/", include("apps.experience.urls")),
#     path("api/", include("apps.achievements.urls")),
#     path("api/timeline/", include("apps.timeline.urls")),

# ]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




