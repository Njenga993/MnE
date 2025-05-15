# urls.py for logframe
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, OutcomeViewSet, OutputViewSet, IndicatorViewSet

router = DefaultRouter()
router.register('goals', GoalViewSet)
router.register('outcomes', OutcomeViewSet)
router.register('outputs', OutputViewSet)
router.register('indicators', IndicatorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
