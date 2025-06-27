# logframe/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ViewSets for API
from .views import GoalViewSet, OutcomeViewSet, OutputViewSet, IndicatorViewSet  # Uncomment if these still exist

# API Router setup
router = DefaultRouter()
router.register('goals', GoalViewSet)
router.register('outcomes', OutcomeViewSet)
router.register('outputs', OutputViewSet)
router.register('indicators', IndicatorViewSet)

urlpatterns = [
    # UI views
    path('', views.logframe_home_view, name='logframe-home'),
    path('goals/', views.goals_view, name='goals-ui'),
    path('outcomes/', views.outcomes_view, name='outcomes-ui'),
    path('outputs/', views.outputs_view, name='outputs-ui'),
    path('indicators/', views.indicators_view, name='indicators-ui'),

    # API endpoints (e.g., /api/v1/logframe/api/goals/)
    path('api/', include(router.urls)),
]
