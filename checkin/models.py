from django.db import models
from django.utils import timezone

# Create your models here.

class CheckinCount(models.Model):
    date = models.DateField(default=timezone.now)
    am_checkins = models.IntegerField(default=0)
    pm_checkins = models.IntegerField(default=0)
    total_checkins =  models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.total_checkins = self.am_checkins + self.pm_checkins
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.date}"

    