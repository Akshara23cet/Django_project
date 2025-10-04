from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser
from patient.models import Patient
from doctor.models import Doctor  # optional, for patient data
from django.http import JsonResponse
from doctor.models import Doctor

def test(request):
       print("hello")
       return redirect('login_page')

# def get_doctors(request):
#       if request.method == "GET":
#         # Fetch all doctors from DB
#          print('hi')
#          doctors = Doctor.objects.all().values("id", "fullname", "specialization")
#         # Convert queryset to list
#          doctor_list = list(doctors)
#          print('doctors => ',doctor_list)

def get_doctors(request):
    selected_spec = request.GET.get('specialization')
    doctors = []

    if selected_spec:
        doctors_qs = Doctor.objects.filter(specialization__iexact=selected_spec)
        doctors = list(doctors_qs.values("id", "fullname"))

    return JsonResponse({'doctors': doctors})

# Registration page
def registration_page(request):
    return render(request, 'registration.html')

# Login page
def login_page(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # creates the session

            # check the role and redirect accordingly
            if user.role == 'doctor':
                return redirect("doctor_dashboard")  # URL name for doctor dashboard
            else:
                return redirect("dashboard")  # URL name for patient dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

# Handle login POST
def signIn(request):
    
    if request.method == 'POST':
        print("ooooooooooo")
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # <--- Important!
            # Redirect based on role
            if user.role == 'patient':
                return redirect('dashboard')
            elif user.role == 'doctor':
                return redirect('doctor_dashboard')
            else:
                return redirect('login_page')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

# Handle registration POST
def register(request):

    if request.method == 'POST':

        role = request.POST.get('role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('registration_page')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )
        print("haaaaaaaaai")

        if role == 'patient':
            patient_name = request.POST.get('patient_name')
            patient_age = request.POST.get('patient_age')
            patient_gender = request.POST.get('patient_gender')
            phone_number = request.POST.get('phone_number')  # make sure field exists in form

            Patient.objects.create(
                user=user,
                first_name=patient_name,  # you can split first/last if needed
                last_name='',
                age=patient_age,
                gender=patient_gender,
                email=email,
                phone_number=phone_number
            )

             # handle doctor registration
        elif role == 'doctor':
            fullname = request.POST.get('doctor_name')
            specialization = request.POST.get('specialization')
            experience = request.POST.get('experience')

            Doctor.objects.create(
                user=user,
                fullname=fullname,
                specialization=specialization,
                experience=experience
            )
        messages.success(request, "Registration successful! Please login.")
        return redirect('login_page')
    return render(request, 'registration.html')
    
    

    
