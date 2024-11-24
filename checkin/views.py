from django.shortcuts import render

# Create your views here.

def checkin_module (request):
    return render(request, "checkin/checkin.html")