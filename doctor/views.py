from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Doctor

#@login_required
def doctor_dashboard(request):
    # Get the logged-in doctor's info
    return render(request, 'dashboard.html')

#@login_required
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'profile.html', {'doctor': doctor})

#@login_required
def doctor_logout(request):
    logout(request)
    return redirect('login/')  # adjust this if your login URL has a different name