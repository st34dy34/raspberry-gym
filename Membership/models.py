from django.db import models
from datetime import timedelta
from django.utils import timezone



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

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPE_CHOICES)
    membership_duration = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES)
    starting_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    expired = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)  # Last updated timestamp

    def calculate_expiration(self):
        duration_mapping = {
            '1 měsíc': timedelta(days=30),
            '3 měsíce': timedelta(days=90),
            '6 měsíců': timedelta(days=180),
            '1 rok': timedelta(days=365),
        }
        return self.starting_date + duration_mapping.get(self.membership_duration, timedelta(0))

    def save(self, *args, **kwargs):
        if self.membership_type == 'časová' and self.starting_date:
            self.expiration_date = self.calculate_expiration()
            self.expired = self.expiration_date < timezone.now().date()
        else:
            self.expiration_date = None
            self.expired = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
