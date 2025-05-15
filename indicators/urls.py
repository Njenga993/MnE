# urls.py for indicators
from django.urls import path
from . import views
from .views import export_indicators_csv, export_indicators_pdf

urlpatterns = [
    path('', views.IndicatorListView.as_view(), name='indicator-list'),
    path('<int:pk>/', views.IndicatorDetailView.as_view(), name='indicator-detail'),
    path('export/indicators/csv/', export_indicators_csv, name='export-indicators-csv'),
    path('export/indicators/pdf/', export_indicators_pdf, name='export-indicators-pdf'),
]