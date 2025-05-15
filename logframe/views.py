# views.py for logframe
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Goal, Outcome, Output, Indicator
from .serializers import GoalSerializer, OutcomeSerializer, OutputSerializer, IndicatorSerializer

def home(request):
    return HttpResponse("Welcome to the M&E System!")

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

