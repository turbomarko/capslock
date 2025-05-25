from django.db import models
from .campaigns import Campaign


class AnalysisResult(models.Model):
    analysis_type = models.CharField(max_length=50)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date_detected = models.DateField()
    severity = models.CharField(max_length=20)
    metric_affected = models.CharField(max_length=50)
    description = models.TextField()
    recommendations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "analysis_results"
        verbose_name = "Analysis Result"
        verbose_name_plural = "Analysis Results"

    def __str__(self):
        return f"{self.campaign.name} - {self.date_detected}"
