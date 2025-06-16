from rest_framework import generics
from .models import Indicator
from .serializers import IndicatorSerializer
from .resources import IndicatorResource
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render


# HTML page view (for rendering the template)
class IndicatorListTemplateView(TemplateView):
    template_name = 'indicators/indicator_list.html'

# API view (returns JSON)
class IndicatorListAPIView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer    

def indicator_detail_page(request, pk):
    indicator = get_object_or_404(Indicator, pk=pk)
    return render(request, 'indicators/indicator_detail.html', {'indicator': indicator})


# CSV export
def export_indicators_csv(request):
    dataset = IndicatorResource().export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indicators.csv"'
    return response

# PDF export
def export_indicators_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="indicators.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Indicator Report")

    y = 780
    for indicator in Indicator.objects.all():
        p.drawString(100, y, f"{indicator.name} - Target: {indicator.target}, Actual: {indicator.actual}")
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = 800

    p.showPage()
    p.save()
    return response

# API views

class IndicatorDetailView(generics.RetrieveAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
