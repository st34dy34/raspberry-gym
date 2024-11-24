from django.db import models
from datetime import timedelta

# Create your models here.

class Member(models.Model):
    MEMBERSHIP_CHOICES = [
        ('1 měsíc', '1 měsíc'),
        ('3 měsíce', '3 měsíce'),
        ('6 měsíců', '6 měsíců'),
        ('1 rok', '1 rok'),
        ('10 vstup', '10 vstupů'),
        ('20 vstup', '20 vstupů'),
        
    ]

    MEMBERSHIP_TYPE_CHOICES = [
        ('vstupová', 'vstupová'),
        ('časová', 'časová'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    membership_type = models.CharField(max_length=50, choices=MEMBERSHIP_TYPE_CHOICES)
    membership_duration = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)
    date = models.DateTimeField(auto_now=True)  # Automatically sets date when updated
    starting_date = models.DateField(null=True, blank=True)  
    expiration_date = models.DateField(null=True, blank=True)  
    expired = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    