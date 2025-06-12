# mobile_api/serializers.py
from rest_framework import serializers
from logframe.models import Goal, Indicator, Outcome, Output

class GoalMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id']  # Only essential fields

class OutcomeMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['id',]   

class OutputMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ['id']               

class IndicatorMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['id', 'name', 'means_of_verification']
