from django.shortcuts import render
from .models import Level
# Create your views here.

def map(request):
    return render(request, 'map/map.html')
