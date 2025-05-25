from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=50)
    objective = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    audience_segment = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "campaigns"
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return self.name
