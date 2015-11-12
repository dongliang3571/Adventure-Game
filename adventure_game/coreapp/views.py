from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf #user security
from django.contrib.auth.models import User

def home(request,message=None):
    context = {}
    context.update(csrf(request))
    return render_to_response('coreapp/home.html',context)

def profile(request):
    return render(request, 'coreapp/profile.html')

def individual(request):
    return render(request, 'coreapp/individual.html')

def story(request):
    return render(request, 'coreapp/story.html')

def login(request):
	context = {}
	context.update(csrf(request))
	return render_to_response('auth/login.html', context)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/profile')
        else:
            return HttpResponseRedirect('/invalid')
    else:
        return HttpResponseRedirect('/invalid')

def invalid_login(request):
	return render_to_response('auth/invalid_login.html')

def logout(request):
    auth.logout(request)
    # context = {'page': 'home'}
    return HttpResponseRedirect('/')

def registration_submission(request):
    username = request.POST.get('username', '')
    firstname = request.POST.get('firstname', '')
    lastname = request.POST.get('lastname', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if len(User.objects.filter(username=username)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, the username %s %s." %(username, "is already taken"))
    if len(User.objects.filter(email=email)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, %s %s." %("there is already an account with email", email))
    user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname) #pylint: disable=E1101
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponseRedirect('/')#'/registration-success')

def registration(request, message=None):
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/registration.html', context)
