from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Doctor

@login_required
def doctor_dashboard(request):
    # Get the logged-in doctor's info
    return render(request, 'dashboard.html')

@login_required
def doctor_profile(request):
    doctor = Doctor.objects.get(user=request.user)
    return render(request, 'profile.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patient.models import Booking  # adjust if your app name differs
from .models import Doctor

@login_required
def doctor_appointments(request):
    user = request.user

    try:
        # find the logged-in doctor object
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return render(request, 'appointments.html', {'error': 'Doctor profile not found'})

    # get all doctors with the same specialization
    same_spec_doctors = Doctor.objects.filter(specialization=doctor.specialization)

    # get bookings for all doctors of that specialization
    appointments = Booking.objects.filter(doctor__in=same_spec_doctors).order_by('date', 'time')

    return render(request, 'appointments.html', {
        'appointments': appointments,
        'doctor': doctor,
    })


# @login_required
# def doctor_logout(request):
#     logout(request)
#     return redirect('login')