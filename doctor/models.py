# doctor/models.py

from django.db import models
from django.conf import settings 

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE
    )

    # Professional details
    specialization = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(default=0)
    department = models.CharField(max_length=50, blank=True, null=True)

    # Availability
    available_from = models.TimeField(blank=True, null=True)
    available_to = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"