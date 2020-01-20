from django.db import models

# Create your models here.
class EnergyUsage(models.Model):
    condo_id = models.CharField(max_length=4)
    peak = models.FloatField(null=True,default='')
    use_amt = models.FloatField(null=True,default='')
    dateTime = models.DateTimeField(auto_now=False)