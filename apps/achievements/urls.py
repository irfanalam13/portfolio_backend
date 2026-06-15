from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, CertificationViewSet

router = DefaultRouter()
router.register(r"achievements", AchievementViewSet)
router.register(r"certifications", CertificationViewSet)

urlpatterns = router.urls
