# urls.py for mobile_api
# mobile_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.GoalListMobileView.as_view(), name='mobile-goals'),
    path('outcomes/', views.OutcomeListMobileView.as_view(), name='mobile-outcomes'),
    path('outputs/', views.OutputListMobileView.as_view(), name='mobile-outputs'),
    path('indicators/', views.IndicatorListMobileView.as_view(), name='mobile-indicators'),
]
