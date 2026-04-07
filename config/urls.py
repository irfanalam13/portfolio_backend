from django.urls import path, include, re_path

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.http import JsonResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)







def custom_404_view(request, exception):
    return JsonResponse(
        {"error": "Not found"},
        status=404
    )


def custom_500_view(request):
    return JsonResponse(
        {
            "error": "Server error",
            "debug": str(request) if settings.DEBUG else None
        },
        status=500
    )


handler404 = "config.urls.custom_404_view"
handler500 = "config.urls.custom_500_view"


urlpatterns = [
    # Admin panel
    path("admin/", admin.site.urls),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0)),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0)),

    path("api/core/", include("apps.core.urls")),

    path("api/projects/", include("apps.projects.urls")),
    path("api/blogs/", include("apps.blog.urls")),
    path("api/skills/", include("apps.skills.urls")),
    path("api/problem_solving", include("apps.problem_solver.urls")),  # problems + solutions
    path("api/contacts/", include("apps.contact.urls")),
    path("api/activity/", include("apps.activity.urls")),
    path("api/ai/", include("apps.ai.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
