from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('logout/', views.doctor_logout, name='doctor_logout'),
]