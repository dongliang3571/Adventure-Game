""" This module handles the user registration, login, family member creation,
and also has the home page view.
"""
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.core.exceptions import PermissionDenied
from django.core.context_processors import csrf #user security
from django.contrib.auth.models import User
from django.template import RequestContext
from .models import Level_num, Game_saved, ContactUs, current_adventures
from .queries import get_logged_in_char, get_all_characters
from .utilities import  get_profile_context, get_adventure_info
from map.models import adventures_info, Adventure, Task


def home(request):
    """This is the home view. It is called when the user goes to the '/' route.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders the template.
    """
    user = request.user
    context = get_adventure_info()
    context.update(csrf(request))
    return render_to_response('coreapp/home.html',
                              context,
                              context_instance=RequestContext(request),)

def adventureslist(request):
    """This is the adventures list view. It is called when the user goes to the '/adventureslist/' route.
    This page lists all of our adventures

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders the template.
    """
    user = request.user
    context = get_adventure_info()

    return render(request, 'coreapp/adventureslist.html',context)

def contact(request):
    """This is the contact view. User reaches this view when he hits the
    send button on the Contact Us form in home page.

    When a visitor fills out the Contact Us
    form and hits the send button in home page, the information is posted to this view which pushes
    to database for admin to view.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseRedirectObject
        Redirects the user to the '/' route after the message is submitted.
    """
    name = request.POST.get('name', '')
    email = request.POST.get('email', '')
    msg = request.POST.get('msg', '')
    ContactUs.objects.create(name=name, email=email, msg=msg)
    messages.success(request, 'Submitted, Thank you!')
    return HttpResponseRedirect('/')

def profile(request):
    """This is the profile view. It is called when the user goes to the '/profile/' route.

    If the user hasn't logged into a char yet, the view renders the individual.html template,
    with a context dictionary created by the function get_profile_context. Otherwise,
    the view will be rendered with a context dictionary that contains the names of all
    the family members attached to the user account as well as the user's last name.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseObject
        Combines a given template with a given context dictionary and renders the template.
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
    request: HttpRequestObject
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

    If credentials are correct, the user is logged in
    and a message is shown confirming user logged in. If account was banned, message
    is shown message telling them account is banned. If credentials are invalid, user is
    told credential is invalid."If credentials are correct, the user is logged in
    and a message is shown confirming user logged in. If account was banned, message
    is shown message telling them account is banned. If credentials are invalid, user is
    told credential is invalid.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseRedirectObject
        Redirects the user to '/' route.
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
    """This is the logout view. It is called when the user hits the logout button.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.


    Returns
    -------
    HttpResponseRedirectObject
        Logs the user out, redirects the user to the '/' view and displays a message
        telling the user they have succesfully logged out.
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')

def registration_submission(request):
    """This is the registration submission view.

    When the user fills out the registration
    form and hits the submit button, the information is posted to this view which creates
    an account for the user with the credentials in the form. Adventure progress is also created.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject
        Redirects the user to the '/' route after user is created.
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
    """This is the registration view. User reaches this view when he hits the
    register button on the login form.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    message: String
        A message that can be passed from one view to another. Used to display incorrect
        credential submission.

    Returns
    -------
    HttpResponseObject
        Combines the registration template with a given context dictionary and renders the template.
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/registration.html', context)

def add_family_member(request, message=None):
    """This is the view for adding a family member. Renders a form for users to
    fill out to add the family member.

    Parameters
    ----------
    request: HttpRequest
        Django request object that contains a variety of information from the middlewares.

    message: String
        A message that can be passed from one view to another. Used to display incorrect
        credential submission.

    Returns
    -------
    HttpResponseObject
        Combines the add family template with a given context dictionary and renders the template.
    """
    context = {}
    context.update(csrf(request))
    if message is not None:
        context['message'] = message
    return render(request, 'auth/addfamily.html', context)

def add_family_member_submission(request):
    """This view handles creating a family character in the database.
    If the user's PIN entry is less than 4 characters or the family member
    already exist in the database, an error message will be shown.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middleware.

    Returns
    -------
    HttpResponseRedirectObject
        Redirects the user to /profile/ is adding family member is succesful.
        Redirects to /add-family-member/ otheriwse.
    """
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
    """This is the invidual view. It handles family member pin authentication. If information
    is invalid it will redirect to /profile/ with an error. If character is already logged
    in and this view is called, the family member is logged out, the profile view is called.

    Parameters
    ----------
    request: HttpRequestOject
        Django request object that contains a variety of information from the middleware.

    Returns
    -------
    HttpResponseRedirectObject or HttpResponseObject
        HttpResponseRedirectObject is returned if family member isn't logged in or pin is invalid.
        HttpResponseObject is returned when user was already logged in and profile() is called.
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
    """This view gets the adventure information from the database and sends it to the front end.

    Parameters
    ----------
    request: HttpRequestObject

    Returns
    -------
    JsonResponseObject
        JSON that contains details about adventure information.
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
