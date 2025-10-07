from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from doctor.models import Doctor
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Booking
from datetime import date




from django.utils import timezone
from .models import Booking


# Create your views here.
@login_required
def dashboard(request):
    upcoming_bookings = Booking.objects.filter(
        patient=request.user,
        date__gte=date.today()
    ).order_by('date', 'time')

    return render(request, 'patient/dashboard.html', {
        'upcoming_bookings': upcoming_bookings,
    })

@login_required
def profile(request):
    return render(request, 'patient/profile.html')  # can create separate profile.html if needed

@login_required
def history(request):
    user = request.user  # current logged-in user
    
    # Fetch all past bookings (before today)
    past_bookings = Booking.objects.filter(
        patient=user,
        date__lt=timezone.now().date()
    ).order_by('-date', '-time')
    
    message = None
    if not past_bookings.exists():
        message = "You have no past bookings."
    
    return render(request, 'patient/history.html', {
        'appointments': past_bookings,
        'message': message
    })
     

def get_doctors(request):
    selected_spec = request.GET.get('specialization')
    doctors = []

    if selected_spec:
        # Filter doctors by specialization (case-insensitive)
        doctors_qs = Doctor.objects.filter(specialization__iexact=selected_spec)
        doctors = list(doctors_qs.values("id", "fullname"))

    return JsonResponse({'doctors': doctors})


# def get_slots(request):
#     doctor_id = request.GET.get("doctor_id")
#     slots = []

#     if doctor_id:
#         now = datetime.now()
#         start_time = now.replace(minute=(0 if now.minute < 30 else 30), second=0, microsecond=0) + timedelta(minutes=30)
#         end_time = now.replace(hour=19, minute=0, second=0, microsecond=0)

#         # Fix here: use doctor=doctor_id
#         booked_slots = Booking.objects.filter(
#             doctor=doctor_id,
#             date=now.date()
#         ).values_list('time', flat=True)

#         while start_time <= end_time:
#             slot_str = start_time.strftime("%I:%M %p")
#             if slot_str not in booked_slots:
#                 slots.append(slot_str)
#             start_time += timedelta(minutes=30)

#     return JsonResponse({"slots": slots})

def get_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')
    
    # Example: available_slots = ["09:00 AM", "10:00 AM", "11:00 AM", ...]
    available_slots = [
        "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
        "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"
    ]
    
    # If date is passed
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()

        # ✅ If selected date is today → show only future slots
        if selected_date == today:
            current_time = datetime.now().time()

            def parse_time(slot_str):
                return datetime.strptime(slot_str, "%I:%M %p").time()

            available_slots = [
                s for s in available_slots if parse_time(s) > current_time
            ]

    return JsonResponse({"slots": available_slots})

def choose_specialization(request):
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    selected_spec = request.GET.get('specialization')
    doctors = None

    if selected_spec:
        # Fetch only doctors with the selected specialization
       # doctors = Doctor.objects.filter(specialization=selected_spec)
            doctors = Doctor.objects.all().values("id", "fullname", "specialization")
            print('fethcing ',doctors)
    context = {
        'specializations': specializations,
        'selected_spec': selected_spec,
        'doctors': doctors
    }

    return render(request, 'patient/choose_specialization.html', context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Booking
from doctor.models import Doctor
from .forms import BookingForm

@login_required
def booking(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Handle booking save via AJAX
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id) if doctor_id else None

        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')
        patient_full_name = request.POST.get('patient_full_name')  # <-- get from form

        # Validate fields
        if not (doctor and date and time and reason and patient_full_name):
            return JsonResponse({"errors": ["All fields are required"]})

        try:
            booking = Booking(
                patient=request.user,
                doctor=doctor,
                date=date,
                time=time,
                reason=reason,
                patient_full_name=patient_full_name  # <-- save full name
            )
            booking.save()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"errors": [str(e)]})

    # For GET request: render the booking form
    specialization = request.GET.get("specialization")
    specializations = Doctor.objects.values_list("specialization", flat=True).distinct()

    form = None
    if specialization:
        doctors = Doctor.objects.filter(specialization=specialization)
        form = BookingForm()
        form.fields['doctor'].queryset = doctors
        # Prefill patient_full_name
        form.fields['patient_full_name'].initial = request.user.get_full_name()

    return render(request, 'patient/booking.html', {
        "form": form,
        "specializations": specializations,
        "specialization": specialization
    })
