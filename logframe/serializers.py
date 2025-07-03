from rest_framework import serializers
from .models import Goal, Outcome, Output, Indicator
from projects.models import Project

class IndicatorSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    output_title = serializers.CharField(source='output.title', read_only=True)

    class Meta:
        model = Indicator
        fields = [
            'id', 'output', 'output_title', 'name', 'means_of_verification',
            'unit_of_measurement', 'baseline', 'target', 'actual', 'progress'
        ]

    def get_progress(self, obj):
        return obj.progress_percentage()


class OutputSerializer(serializers.ModelSerializer):
    indicators = IndicatorSerializer(many=True, read_only=True)
    outcome_title = serializers.CharField(source='outcome.title', read_only=True)

    class Meta:
        model = Output
        fields = [
            'id', 'title', 'description', 'outcome', 'outcome_title', 'indicators'
        ]


class OutcomeSerializer(serializers.ModelSerializer):
    outputs = OutputSerializer(many=True, read_only=True)
    goal_title = serializers.CharField(source='goal.title', read_only=True)

    class Meta:
        model = Outcome
        fields = [
            'id', 'title', 'description', 'goal', 'goal_title', 'outputs'
        ]


class GoalSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Goal
        fields = ['id', 'title', 'description', 'created_at', 'project', 'project_name']
class ProjectSerializer(serializers.ModelSerializer):
    goals = GoalSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'goals']
