from django.urls import path
from .views import (
    IndicatorListView,
    IndicatorDetailView,
    export_indicators_csv,
    export_indicators_pdf,
)

app_name = "indicators"

urlpatterns = [
    path('', IndicatorListView.as_view(), name='list'),
    path('<int:pk>/', IndicatorDetailView.as_view(), name='detail'),
    path('export/csv/', export_indicators_csv, name='export_csv'),
    path('export/pdf/', export_indicators_pdf, name='export_pdf'),
]
