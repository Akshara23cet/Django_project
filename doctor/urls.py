# doctor/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('profile/', views.doctor_profile, name='doctor_profile'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]