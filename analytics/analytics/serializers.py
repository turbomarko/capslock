from rest_framework import serializers

from .models import AnalysisResult


class AnalysisResultSerializer(serializers.ModelSerializer):
    campaign = serializers.CharField(source="campaign.name")

    class Meta:
        model = AnalysisResult
        fields = "__all__"


class AnalysisResultListSerializer(serializers.ModelSerializer):
    campaign = serializers.CharField(source="campaign.name")

    class Meta:
        model = AnalysisResult
        fields = [
            'id',
            'date_detected',
            'campaign',
            'analysis_type',
            'severity',
            'metric_affected'
        ]
