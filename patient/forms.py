from django import forms
from .models import Booking
from doctor.models import Doctor

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        specialization = kwargs.pop('specialization', None)
        super().__init__(*args, **kwargs)
        if specialization:
            # Case-insensitive filter to avoid mismatch
            self.fields['doctor'].queryset = Doctor.objects.filter(specialization__iexact=specialization)
        else:
            self.fields['doctor'].queryset = Doctor.objects.none()
