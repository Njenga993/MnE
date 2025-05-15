# urls.py for dashboard
from django.urls import path
from .views import DashboardSummaryView

urlpatterns = [
     path('', DashboardSummaryView.as_view(), name='dashboard-home'), 
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
]
