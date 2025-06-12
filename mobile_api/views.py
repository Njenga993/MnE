# views.py for mobile_api
from rest_framework import generics
from logframe.models import Goal, Indicator, Outcome, Output
from .serializers import GoalMobileSerializer, IndicatorMobileSerializer, OutcomeMobileSerializer, OutputMobileSerializer 

class GoalListMobileView(generics.ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalMobileSerializer

class OutcomeListMobileView(generics.ListAPIView):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeMobileSerializer

class OutputListMobileView(generics.ListAPIView):
    queryset = Output.objects.all()
    serializer_class = OutputMobileSerializer
                

class IndicatorListMobileView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorMobileSerializer
