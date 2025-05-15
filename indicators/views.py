# views.py for indicators
# indicators/views.py
from rest_framework import generics
from .models import Indicator
from .serializers import IndicatorSerializer
from .resources import IndicatorResource
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_indicators_csv(request):
    dataset = IndicatorResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indicators.csv"'
    return response

def export_indicators_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="indicators.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Indicator Report")

    y = 780
    for indicator in Indicator.objects.all():
        p.drawString(100, y, f"{indicator.name} - {indicator.description} - Target: {indicator.target}")
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

    p.showPage()
    p.save()
    return response

class IndicatorListView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class IndicatorDetailView(generics.RetrieveAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
