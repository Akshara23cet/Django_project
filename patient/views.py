from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
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
    message = None

    # Fetch all past bookings (before current time)
    past_bookings = Booking.objects.filter(
        patient=user,
        date__lt=timezone.now().date()
    ).order_by('-date', '-time')

    if not past_bookings.exists():
        message = "You have no past bookings."

    return render(request, 'patient/history.html', {
        'appointments': past_bookings,
        'message': message
    })

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
