from rest_framework.routers import DefaultRouter
from .views import ProblemViewSet, AnswerViewSet, TagViewSet

router = DefaultRouter()
router.register("problems", ProblemViewSet)
router.register("answers", AnswerViewSet)
router.register("tags", TagViewSet)

urlpatterns = router.urls