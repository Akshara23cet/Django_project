# doctor/models.py

from django.db import models
from django.conf import settings # <-- 1. Import settings is necessary

class Doctor(models.Model):
    # Link to the custom user model defined in settings.AUTH_USER_MODEL
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <-- 2. The FIX: References your CustomUser model
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
        # This assumes your CustomUser model has 'first_name' and 'last_name' fields
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.specialization}"