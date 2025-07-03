# views.py for reports
import csv
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from logframe.models import Indicator

def export_indicators_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indicators.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Description'])  # Adapt as needed

    for ind in Indicator.objects.all():
        writer.writerow([ind.id, ind.name, ind.description])

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
