from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf #user security


def home(request):
    return render(request, 'coreapp/home.html')


def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('auth/login.html', c)


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    # if user is not None:
    #
    # else:
