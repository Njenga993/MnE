# mobile_api/serializers.py
from rest_framework import serializers
from logframe.models import Goal, Indicator

class GoalMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name']  # Only essential fields

class IndicatorMobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = ['id', 'name', 'means_of_verification']
