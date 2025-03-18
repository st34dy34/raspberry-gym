from django.db import models
from django.utils import timezone

class CheckinCountManager(models.Manager):
    def get_today(self):
        today = timezone.now().date()
        return self.get_or_create(date=today)
    
    def get_date_range(self, start_date, end_date):
        return self.filter(date__gte=start_date, date__lte=end_date)

class CheckinCount(models.Model):
    date = models.DateField(default=timezone.now, db_index=True)  # Added index
    am_checkins = models.IntegerField(default=0)
    pm_checkins = models.IntegerField(default=0)
    total_checkins = models.IntegerField(default=0)
    
    # Add the custom manager
    objects = CheckinCountManager()
    
    def save(self, *args, **kwargs):
        self.total_checkins = self.am_checkins + self.pm_checkins
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"{self.date}"