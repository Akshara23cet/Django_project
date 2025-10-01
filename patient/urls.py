from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('settings/', views.settings, name='settings'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
