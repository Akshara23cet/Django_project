from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Patient(models.Model):
    # Link to Django user (foreign key, you can manually insert user_id)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="patients"
)

    # Basic patient details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # Medical info
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Booking(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.doctor} on {self.date}"
    
class Doctor(models.Model):
        fullname = models.CharField(max_length=100)
        specialization = models.CharField(max_length=50)

        def __str__(self):
           return self.fullname