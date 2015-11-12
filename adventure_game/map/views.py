from django.shortcuts import render
from .models import Level
# Create your views here.

def index(request):
    if Level.objects.all()[0]:
        ln = Level.objects.all()[0].level_number;
        if ln==0:
            boyn="boy"
        elif ln==1:
            boyn="boy boy1"
        elif ln==2:
            boyn="boy boy1 boy2"
        elif ln==3:
            boyn="boy boy1 boy2 boy3"
        elif ln==4:
            boyn="boy boy1 boy2 boy3 boy4"
        return render(request, 'map/index.html',{'boyn':boyn})
    else:
        boyn="boy"
        return render(request, 'map/index.html',{'boyn':boyn})

def task1(request):
    return render(request,'map/task1.html')

def task2(request):
    return render(request,'map/task2.html')
