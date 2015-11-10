from django.shortcuts import render
from .models import Level
# Create your views here.

def index(request):
    return render(request, 'map/index.html')
