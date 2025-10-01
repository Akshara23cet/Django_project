from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CustomUser  # import your custom user model
from django.contrib import messages
from patient.models import Patient  # or DoctorDetails



def registration_page(request)
    return render(request, 'registration.html')


def login_page(request):
    return render(request, 'login.html')


def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # redirect to home page after login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        # ----------------------------
        # Step 1: Fetch all input values
        # ----------------------------
        role = request.POST.get('role')  # patient or doctor
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Patient fields
        patient_name = request.POST.get('patient_name')
        patient_age = request.POST.get('patient_age')
        patient_gender = request.POST.get('patient_gender')

        # Doctor fields
        doctor_name = request.POST.get('doctor_name')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')

        # ----------------------------
        # Step 1.1: Basic validation
        # ----------------------------
        if not username or not email or not password:
            messages.error(request, "Username, email, and password are required.")
            return redirect('register')

        if role == 'patient':
            if not patient_name or not patient_age or not patient_gender:
                messages.error(request, "All patient fields are required.")
                return redirect('register')

        elif role == 'doctor':
            if not doctor_name or not specialization or not experience:
                messages.error(request, "All doctor fields are required.")
                return redirect('register')

        else:
            messages.error(request, "Invalid role selected.")
            return redirect('register')

        # ----------------------------
        # Step 2: Check if username exists
        # ----------------------------
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        # ----------------------------
        # Step 3: Create user
        # ----------------------------
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # ----------------------------
        # Step 4: Role-specific table insertion (optional)
        # ----------------------------
        '''
        if role == 'patient':
            Patient.objects.create(
                user=user,
                full_name=patient_name,
                age=patient_age,
                gender=patient_gender
            )
        elif role == 'doctor':
            speciality_obj, created = Speciality.objects.get_or_create(name=specialization)
            Doctor.objects.create(
                user=user,
                full_name=doctor_name,
                speciality=speciality_obj,
                experience_years=experience
            )
        '''

        messages.success(request, "Registration successful! Please login.")
        return redirect('login_page')

    return render(request, 'registration.html')
