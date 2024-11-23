from django.db import models

# Create your models here.

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    membership_type = models.CharField(max_length=50)
    join_date = models.DateTimeField(auto_now_add=True)  # Automatically sets the join date
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    