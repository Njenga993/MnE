# views.py for mobile_api
from rest_framework import generics
from logframe.models import Goal, Indicator
from .serializers import GoalMobileSerializer, IndicatorMobileSerializer

class GoalListMobileView(generics.ListAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalMobileSerializer

class IndicatorListMobileView(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorMobileSerializer
