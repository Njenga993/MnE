from . import views
from django.urls import path
from .views import (
    IndicatorListTemplateView,
    IndicatorListAPIView,
    IndicatorDetailView,
    export_indicators_csv,
    export_indicators_pdf,
    
)

urlpatterns = [
    path('indicators/', IndicatorListTemplateView.as_view(), name='indicator_list_page'),
    path('api/v1/indicators/', IndicatorListAPIView.as_view(), name='indicator_list_api'),
    path('api/v1/indicators/<int:pk>/', IndicatorDetailView.as_view(), name='indicator_detail_api'),
    path('indicators/<int:pk>/', views.indicator_detail_page, name='indicator-detail'),
    path('indicators/export/csv/', export_indicators_csv, name='export_indicators_csv'),
    path('indicators/export/pdf/', export_indicators_pdf, name='export_indicators_pdf'),
]
