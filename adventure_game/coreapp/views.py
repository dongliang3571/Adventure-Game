from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf #user security


def home(request):
    return render(request, 'coreapp/home.html')

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
            return HttpResponseRedirect('/')
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
