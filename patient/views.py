from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from doctor.models import Doctor
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Booking




from django.utils import timezone
from .models import Booking


# Create your views here.
@login_required
def dashboard(request):
   
   return render(request, 'patient/dashboard.html')

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
#     doctor_id = request.GET.get('doctor_id')
#     now = datetime.now()

#     # Define fixed slots for a day (dummy schedule)
#     slots = [
#         "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
#         "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"
#     ]

#     # Filter out past slots based on current time
#     available_slots = []
#     for s in slots:
#         slot_time = datetime.strptime(s, "%I:%M %p").time()
#         if slot_time > now.time():  # only future slots
#             available_slots.append(s)

#     return JsonResponse({"slots": available_slots})

def get_slots(request):
    doctor_id = request.GET.get("doctor_id")
    slots = []

    if doctor_id:
        now = datetime.now()
        start_time = now.replace(minute=(0 if now.minute < 30 else 30), second=0, microsecond=0) + timedelta(minutes=30)
        end_time = now.replace(hour=19, minute=0, second=0, microsecond=0)

        # Fix here: use doctor=doctor_id
        booked_slots = Booking.objects.filter(
            doctor=doctor_id,
            date=now.date()
        ).values_list('time', flat=True)

        while start_time <= end_time:
            slot_str = start_time.strftime("%I:%M %p")
            if slot_str not in booked_slots:
                slots.append(slot_str)
            start_time += timedelta(minutes=30)

    return JsonResponse({"slots": slots})


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



# @login_required
# def booking(request):
#     specialization = request.GET.get('specialization')
#     specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
#     form = BookingForm(specialization=specialization) if specialization else None
#     if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         doctor_id = request.POST.get('doctor')
#         date = request.POST.get('date')
#         time = request.POST.get('time')
#         reason = request.POST.get('reason')

#         if not (doctor_id and date and time and reason):
#             return JsonResponse({"errors": ["All fields are required"]})

#         try:
#             booking = Booking(
#                 patient=request.user,
#                 doctor_id=doctor_id,   # <-- this maps to doctor foreign key
#                 date=date,
#                 time=time,
#                 reason=reason
#             )
#             booking.save()
#             return JsonResponse({"success": True})
#         except Exception as e:
#             return JsonResponse({"errors": [str(e)]})
        
#         return render(request, 'patient/booking.html', {
#          'specializations': specializations,
#          'specialization': specialization,
#       'form': form,
#      })


    # AJAX POST submission
    # if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     form = BookingForm(request.POST, specialization=request.POST.get('specialization'))
    #     if form.is_valid():
    #         booking = form.save(commit=False)
    #         booking.patient = request.user
    #         booking.save()
    #         return JsonResponse({'success': True})
    #     else:
    #         errors = [f"{k}: {v[0]}" for k, v in form.errors.items()]
    #         return JsonResponse({'success': False, 'errors': errors})

    # return render(request, 'patient/booking.html', {
    #     'specializations': specializations,
    #     'specialization': specialization,
    #     'form': form,
    # })

@login_required
def booking(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # handle booking save via AJAX
        doctor_id = request.POST.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)

        date = request.POST.get('date')
        time = request.POST.get('time')
        reason = request.POST.get('reason')

        if not (doctor_id and date and time and reason):
            return JsonResponse({"errors": ["All fields are required"]})

        try:
            booking = Booking(
                patient=request.user,
                doctor=doctor,
                date=date,
                time=time,
                reason=reason
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

    return render(request, 'patient/booking.html', {
        "form": form,
        "specializations": specializations,
        "specialization": specialization
    })
