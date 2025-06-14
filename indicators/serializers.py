from rest_framework import serializers
from .models import Indicator

class IndicatorSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Indicator
        fields = '__all__'  # Or list fields manually if you prefer control

    def get_progress(self, obj):
        if obj.target:
            return round((obj.actual / obj.target) * 100, 2)
        return 0
