from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf #user security
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import Level_num, Game_saved
from .queries import get_logged_in_char, get_all_characters
from .utilities import  get_profile_context, get_adventure_info
from map.models import adventures_info, Adventure, Task

def home(request):
    """This is the home view. It is called when the user goes to the '/' route.

    Parameters
    ----------
    request: HttpRequest
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders the template.
    """

    context = get_adventure_info()
    context.update(csrf(request))
    return render_to_response('coreapp/home.html',
                              context,
                              context_instance=RequestContext(request))

def profile(request):
    """This is the profile view. It is called when the user goes to the '/profile/' route.

    Parameters
    ----------
    request: HttpRequest
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders the template.
        If the user hasn't logged into a char yet, the view renders the individual.html template,
        with a context dictionary created by the function get_profile_context. Otherwise,
        the view will be rendered with a context dictionary that contains the names of all
        the family members attached to the user account as well as the user's last name.
    """
    user = request.user
    characters = get_all_characters(user)
    if get_logged_in_char(characters):
        context = get_profile_context(user, characters)
        return render(request, 'coreapp/individual.html', context)
    else:
        family_members = characters
        userlname = user.last_name
        context = {'family_members' : family_members,
                   'lastname' : userlname,
                  }
        return render(request, 'coreapp/profile.html', context)

def story(request):
    """This is the story view. It is called when the user goes to the '/story' route.

    Parameters
    ----------
    request: HttpRequest
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders
        the story.html template.
    """
    return render(request, 'coreapp/story.html')

def auth_view(request):
    """This is the story view. It handles user login authentication.

    Parameters
    ----------
    request: HttpRequest
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseRedirectObject
        Redirects the user to '/' route. If credentials are correct, the user is logged in
        and a message is shown confirming user logged in. If account was banned, message
        is shown message telling them account is banned. If credentials are invalid, user is
        told credential is invalid."If credentials are correct, the user is logged in
        and a message is shown confirming user logged in. If account was banned, message
        is shown message telling them account is banned. If credentials are invalid, user is
        told credential is invalid.
    """

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            messages.success(request, 'Hi %s, you have successfully logged in.' %(user.last_name))
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'Your account has been banned,' \
                             ' please contact us to re-activate your account!')
            return HttpResponseRedirect('/')
    else:
        messages.success(request, 'The account you entered is invalid, please try again!')
        return HttpResponseRedirect('/')

def logout(request):
    """
    The user is sent here when they logout. They are then redirected to the home page.
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')

def registration_submission(request):
    """
    A visitor is sent to this page when they submit their registration.
    After being registered they are redirected to the home page.
    """
    username = request.POST.get('username', '')
    firstname = request.POST.get('firstname', '')
    lastname = request.POST.get('lastname', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    if len(User.objects.filter(username=username)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, the username %s %s."
                            % (username, "is already taken"))
    if len(User.objects.filter(email=email)) != 0: #pylint: disable=E1101
        return registration(request, "Try again, %s %s."
                            % ("there is already an account with that email", email))
    user = User.objects.create_user(username=username, email=email, password=password,
                                    first_name=firstname, last_name=lastname) #pylint: disable=E1101
    first_char = user.character_set.create(character_name="pin#1111", character_pin="1111")
    first_char.is_logged = True
    first_char.save()
    Level_num.objects.create(user=user, user_point=0, user_level=1)
    Game_saved.objects.create(user=user, adventure_saved="", task_saved="")
    user = auth.authenticate(username=username, password=password)
    auth.login(request, user)
    return HttpResponseRedirect('/')

def registration(request, message=None):
    """
    A visitor can register here and submit the registration form.
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/registration.html', context)

def add_family_member(request, message=None):
    """
    The user can add family members to their account here
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/addfamily.html', context)

def add_family_member_submission(request):
    full_name = request.POST.get('member-name', '')
    pin = request.POST.get('member-pin', '')
    if len(pin) != 4:
        messages.success(request, 'Please enter 4 characters as your PIN number')
        return HttpResponseRedirect('/add-family-member/')
    else:
        current_user = request.user
        if current_user.character_set.filter(character_name=full_name):
            messages.success(request, 'This member has already been added, try another name')
            return HttpResponseRedirect('/add-family-member/')
        else:
            current_user.character_set.create(character_name=full_name, character_pin=pin)
            return HttpResponseRedirect('/profile/')


def individual(request):
    """
    The user is sent to here after enter thier own pin # for selected member
    """
    user = request.user
    character_name = request.POST.get('character_name', '')
    character_pin = request.POST.get('character_pin', '')
    characters = get_all_characters(user)

    if get_logged_in_char(characters):
        char = get_logged_in_char(characters)[0]
        char.is_logged = False
        char.save()
        return profile(request)

    if user.character_set.filter(character_name=character_name, character_pin=character_pin):
        char = user.character_set.filter(character_name=character_name,
                                         character_pin=character_pin)[0]
        char.is_logged = True
        char.save()
        return HttpResponseRedirect('/profile/')
    else:
        messages.success(request, 'The PIN you entered is incorrect or did not' \
                         ' select your family role, please try again!')
        return HttpResponseRedirect('/profile/')

def get_adventure_detail(request):
    """
    This function pass adventure details in json format to front end for ajax to receive them.
    """
    if request.is_ajax():
        user = request.user
        game_saved = user.game_saved
        adventure_id = game_saved.adventure_saved
        task_num = game_saved.task_saved
        adventure = Adventure.objects.get(adventure_id=adventure_id)
        Adventures_info = adventures_info.objects.get(adventure_name=adventure)
        task = Task.objects.get(adventure_name=adventure, task_number=task_num)


        alist =[
                {
                    "name" : str(adventure.adventure_name),
                    "items" : str(Adventures_info.items_needed),
                    "expenses" : str(Adventures_info.expenses),
                    "locations" : Adventures_info.locations,
                    "mapaddress" : str(task.google_map),
                    "theme_character_url" : str(adventure.theme_character_url)
                }

                ]

        return JsonResponse(alist, safe=False)
    else:
        raise PermissionDenied()

#for testing only
def usejson(request):

    return render(request, 'coreapp/getjson.html', {"usea":"hahah"})
