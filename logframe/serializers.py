from rest_framework import serializers
from .models import Goal, Outcome, Output, Indicator

class IndicatorSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Indicator
        fields = [
            'id', 'output', 'name', 'means_of_verification',
            'unit_of_measurement', 'baseline', 'target', 'actual', 'progress'
        ]

    def get_progress(self, obj):
        return obj.progress_percentage()

class OutputSerializer(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)

    class Meta:
        model = Output
        fields = '__all__'

class OutcomeSerializer(serializers.ModelSerializer):
    outputs = OutputSerializer(many=True, read_only=True)

    class Meta:
        model = Outcome
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    outcomes = OutcomeSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
