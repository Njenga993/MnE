# views.py for reports
import csv
from django.http import HttpResponse
from indicators.models import Indicator  # use your actual model path

def export_indicators_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="indicators.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Description'])  # Adapt as needed

    for ind in Indicator.objects.all():
        writer.writerow([ind.id, ind.name, ind.description])

    return response

