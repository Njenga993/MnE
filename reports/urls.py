# urls.py for reportsfrom django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('export/indicators/csv/', views.export_indicators_csv, name='export-indicators-csv'),
    path('export/indicators/pdf/', views.export_indicators_pdf, name='export-indicators-pdf'),
]
