

# urls.py for logframe
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, OutcomeViewSet, OutputViewSet, IndicatorViewSet

router = DefaultRouter()
router.register('goals', GoalViewSet)
router.register('outcomes', OutcomeViewSet)
router.register('outputs', OutputViewSet)
router.register('indicators', IndicatorViewSet)

urlpatterns = [
    path('', views.logframe_home_view, name='logframe-home'),  # Template view
    path('goals/', views.goals_view, name='goals-ui'),
    path('outcomes/', views.outcomes_view, name='outcomes-ui'),
    path('outputs/', views.outputs_view, name='outputs-ui'),
    path('indicators/', views.indicators_view, name='indicators-ui'),
    path('api/', include(router.urls)),  # Now your API lives under /api/v1/logframe/api/
]


