from django.db import models

# Create your models here.
class EnergyUsage(models.Model):
    condo_id = models.CharField(max_length=4)
    peak = models.FloatField()
    use_amt = models.FloatField()
    dateTime = models.DateTimeField(auto_now=False)