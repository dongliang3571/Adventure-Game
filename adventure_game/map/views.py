from django.shortcuts import render
from .models import Level
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
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
        messages.warning(request, 'Welcome to your adventures')
        return render(request, 'map/index.html',{'boyn':boyn})
    else:
        messages.warning(request, 'Please Sign in')
        return HttpResponseRedirect(reverse('coreapp:home'))

def task1(request):
    return render(request,'map/task1.html')

def task1_question1(request):
    ans = request.GET.get('answer','')
    if ans:
        if ans=='2':
            l = request.user.level
            l.level_number=1
            l.save()
            return render(request, 'map/task1_1.html',{'message':'Congradulations, Your answer is correct!!!'})
        else:
            return render(request, 'map/task1_1.html',{'message2':'Sorry, Your answer is Wrong, Try again....','after':'show'})
    else:
        return render(request, 'map/task1_1.html',{'after':'show'})


def task2(request):
    return render(request,'map/task2.html')
