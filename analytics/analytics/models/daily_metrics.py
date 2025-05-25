from django.db import models
from .campaigns import Campaign


class DailyMetric(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    date = models.DateField()
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    conversions = models.IntegerField()
    spend = models.DecimalField(max_digits=10, decimal_places=2)
    ctr = models.FloatField()  # Click-through rate
    cpc = models.FloatField()  # Cost per click
    cpa = models.FloatField()  # Cost per acquisition
    roas = models.FloatField() # Return on ad spend
    device_breakdown = models.JSONField()
    geography = models.JSONField()

    class Meta:
        db_table = "daily_metrics"
        verbose_name = "Daily Metric"
        verbose_name_plural = "Daily Metrics"

    def __str__(self):
        return f"{self.campaign.name} - {self.date}"
