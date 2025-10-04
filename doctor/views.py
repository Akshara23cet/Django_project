

## Create your views here.
## doctor/views.py
from django.shortcuts import render

def doctor_dashboard(request):
   return render(request, 'docDash.html')  # create this template



    
