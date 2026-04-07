from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, github_activity

router = DefaultRouter()
router.register("", ActivityViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("github/", github_activity),
]