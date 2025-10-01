from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    # Link to Django user (optional, if you want login for patients)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Basic patient details
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices, default='O')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    # Medical info
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
