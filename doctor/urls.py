# doctor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]
