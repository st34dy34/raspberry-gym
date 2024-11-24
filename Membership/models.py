from django.db import models
from datetime import timedelta
from django.utils import timezone

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
    
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
    ]
    expired = models.BooleanField(default=True)
    
    def calculate_expiration(self):
        duration_mapping = {
            '1 měsíc': timedelta(days=30),
            '3 měsíce': timedelta(days=90),
            '6 měsíců': timedelta(days=180),
            '1 rok': timedelta(days=365),
        }
        return self.starting_date + duration_mapping.get(self.membership_duration, timedelta(0))
    
    
    def save(self, *args, **kwargs):
        # Check if the membership type is time 
        if self.membership_type == "časová" and self.starting_date and self.membership_duration:
            self.expiration_date = self.calculate_expiration()
        else:
            self.expiration_date = None  # Clear expiration date if not "časová"

        # Update expired field only if expiration_date is set
        if self.expiration_date:
            self.expired = self.expiration_date < timezone.now().date()
        else:
            self.expired = False  # Default to False if expiration_date is not applicable

        super().save(*args, **kwargs)  # Call the parent save method
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    