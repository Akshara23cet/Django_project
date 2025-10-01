from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def dashboard(request):
   
   return render(request, 'patient/dashboard.html')

@login_required
def profile(request):
    return render(request, 'patient/profile.html')  # can create separate profile.html if needed

@login_required
def history(request):
    return render(request, 'patient/history.html')  # can create separate history.html

@login_required
def settings(request):
    return render(request, 'patient/settings.html')  # can create separate settings.html
