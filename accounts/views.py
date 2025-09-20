from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from patient.models import Patient  # or DoctorDetails
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')   # redirect to home page after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def register(request):
    return render(request,'registration.html')
