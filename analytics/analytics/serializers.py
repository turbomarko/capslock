from rest_framework import serializers

from .models import AnalysisResult


class AnalysisResultSerializer(serializers.ModelSerializer):
    campaign = serializers.CharField(source="campaign.name")

    class Meta:
        model = AnalysisResult
        fields = "__all__"
