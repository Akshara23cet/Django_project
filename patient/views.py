from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BookingForm

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
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = request.user  # assign logged-in patient
            booking.save()
            return redirect('patient_dashboard')  # redirect after success
    else:
        form = BookingForm()
    return render(request, 'patient/booking.html', {'form': form})

# doctor/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#from .models import Doctor # Import your Doctor model
#from patient.models import Appointment # Import the Appointment model from the patient app
from django.http import Http404 # Useful for cleaner error handling

@login_required
def view_appointments(request):
    """
    Retrieves and displays all appointments scheduled for the logged-in doctor.
    """
    
    try:
        # 1. Get the Doctor profile linked to the current user
        # This assumes your Doctor model has a ForeignKey to CustomUser named 'user'
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # If the logged-in user isn't linked to a Doctor profile, treat it as a permission error.
        raise Http404("Doctor profile not found for this user.")

    # 2. Fetch all appointments where the 'doctor' field points to this doctor object.
    # Order them by date and time for a chronological schedule.
    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('appointment_date', 'appointment_time')

    context = {
        'doctor': doctor,
        'appointments': appointments,
        'appointment_count': appointments.count(),
        'title': 'My Schedule',
    }
    
    # The template name should be plural for clarity
    return render(request, 'appointments/doctor_appointments.html', context)