from django.shortcuts import render
from .models import Level
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    user=request.user
    if(user.is_authenticated()):
        ln=user.level.level_number
        
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
        return HttpResponseRedirect(reverse('coreapp:home'))

def task1(request):
    return render(request,'map/task1.html')

def task2(request):
    return render(request,'map/task2.html')
