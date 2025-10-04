from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('booking/', views.booking, name='booking'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('book-appointment/', views.choose_specialization, name='choose_specialization'),
    path('choose-specialization/', views.choose_specialization, name='choose_specialization'),
    path('get-doctors/', views.get_doctors ,name='get_doctors'),
    path('get-slots/', views.get_slots, name='get_slots'),
    path('booking/', views.booking, name='patient_booking'),





]
