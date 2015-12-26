from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import Adventure
from .models import Task
from .models import Question
from .models import Answer
from coreapp.models import Level_num
from coreapp.models import Track
from coreapp.models import Game_saved
from coreapp.models import current_adventures
from .models import adventures_info
import json

# Create your views here.

def map(request):
    """
    This is the map view, it collect a list of context and is pass along with
    map.html which renders entire map where users can see their adventures progress.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject or HttpResponseObject
        It returns HttpResponseRedirectObject when user have not yet create a family member.
        It returns HttpResponseObject when user is logged in and have family member created.
    """
    user = request.user
    adventureid = request.GET.get('adventureid', '')
    if user.is_authenticated():
        if not user.character_set.all():
            messages.warning(request, 'Create your family roles so that you can start your adventures.')
            return HttpResponseRedirect(reverse('coreapp:profile'))
        else:
            if user.game_saved.adventure_saved:
                task_saved = str(user.game_saved.task_saved)
                adventure_saved = user.game_saved.adventure_saved
                adv = Adventure.objects.get(adventure_id = adventure_saved)
                tasks = Task.objects.filter(adventure_name = adv).order_by("id")
                task_list = []
                for task in tasks:
                    task_list_context = {
                        "id_of_task": task.id_of_task,
                        "place_img_url": task.place_img_url,
                        "name_of_location": task.name_of_location
                    }
                    task_list.append(task_list_context)
                boyn = ""
                if task_saved == "1":
                    boyn = "boy"
                elif task_saved == "2":
                    boyn = "boy boy1"
                elif task_saved == "3":
                    boyn = "boy boy1 boy2"
                elif task_saved == "4":
                    boyn = "boy boy1 boy2 boy3"
                elif task_saved == "5":
                    boyn = "boy boy1 boy2 boy3 boy4"
                messages.warning(request, 'Welcome to your adventures')
                context = {
                    "boyn" : boyn,
                    "tasks" : task_list,
                    "number_of_task" : len(tasks)

                }
                return render(request, 'map/map.html', context)
            else:
                messages.warning(request, 'Select your adventure to continue.')
                return HttpResponseRedirect('/profile')
    else:
        messages.warning(request, 'Please sign in')
        return HttpResponseRedirect(reverse('coreapp:home'))


def beginingstory(request):
    """
    This function takes user to a infromational page which gives details of specific
    adventure and only displays once when users first begin the adventure.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject or HttpResponseObject
        It returns HttpResponseRedirectObject when user is currently playing this adventure.
        It returns HttpResponseObject when user is first time playing this adventure
    """
    user = request.user
    adventureid = request.GET.get('adventureid', '')
    Current_adventures = current_adventures.objects.filter(user = user)

    if Current_adventures:
        current_adventure = Current_adventures.filter(adventure_saved = adventureid)
        if current_adventure:
            game_saved = user.game_saved
            game_saved.adventure_saved = current_adventure[0].adventure_saved
            game_saved.task_saved = current_adventure[0].task_saved
            game_saved.save()
            return HttpResponseRedirect(reverse('map:map'))
        else:
            adventure = Adventure.objects.get(adventure_id = adventureid)
            Adventures_info = adventures_info.objects.get(adventure_name = adventure)
            context = {
                "adventure_title" : adventure.adventure_name,
                "items_needed" : Adventures_info.items_needed,
                "expenses" : Adventures_info.expenses,
                "locations" : Adventures_info.locations,
                "map_address" : Adventures_info.map_address,
                "adventureid" : adventureid,
                "theme_character_url" : str(adventure.theme_character_url),
                "adventure_description" : adventure.adventure_description
            }

            return render(request, 'map/details.html',context)

    else:
        adventure = Adventure.objects.get(adventure_id = adventureid)
        Adventures_info = adventures_info.objects.get(adventure_name = adventure)
        context = {
            "adventure_title" : adventure.adventure_name,
            "items_needed" : Adventures_info.items_needed,
            "expenses" : Adventures_info.expenses,
            "locations" : Adventures_info.locations,
            "map_address" : Adventures_info.map_address,
            "adventureid" : adventureid,
            "theme_character_url" : str(adventure.theme_character_url),
            "adventure_description" : adventure.adventure_description
        }

        return render(request, 'map/details.html',context)

def visitorview(request):
    """
    This function is triggered when user hit the adventure shown on homepage,
    which is showing user the adventures' detail even a user is not logged in.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseObject
        It always returns HttoResponseObject along with a list of context dictionary
        collected from user.
    """
    adventureid = request.GET.get('adventureid', '')

    adventure = Adventure.objects.get(adventure_id = adventureid)
    Adventures_info = adventures_info.objects.get(adventure_name = adventure)
    context = {
        "adventure_title" : adventure.adventure_name,
        "items_needed" : Adventures_info.items_needed,
        "expenses" : Adventures_info.expenses,
        "locations" : Adventures_info.locations,
        "map_address" : Adventures_info.map_address,
        "adventureid" : adventureid,
        "theme_character_url" : str(adventure.theme_character_url),
        "adventure_description" : adventure.adventure_description
    }

    return render(request, 'map/visitorview.html',context)


def save_current(request):
    """
    This function is triggered when a user decides to play a specific adventure
    and hits the button at the bottom of the detail.html. This update a user's
    information in database(e.g. save which adventure he/she is playing).

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject
        It always returns HttoResponseRedirectObject, it redirects user to map page.
    """
    adventureid = request.GET.get('adventureid', '')
    user = request.user
    game_saved = user.game_saved
    game_saved.adventure_saved = adventureid
    game_saved.task_saved = '1'
    game_saved.save()
    current_adventures.objects.create(user=user, adventure_saved=adventureid, task_saved='1')

    return HttpResponseRedirect(reverse('map:map'))


def task(request):
    """
    This function retrives tasks from database and displays on task pages for users to complete.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseObject
        It always returns HttoResponseObjects along with a list of context dictionary
        collected from task information in database.
    """

    user = request.user
    game_saved = user.game_saved
    adventure_saved = game_saved.adventure_saved
    task_saved = game_saved.task_saved
    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)

    task_detail = task.task_detail
    task_ans = task.task_ans
    task_type = str(task.task_type)
    task_description = task.task_description
    show_textbox = ''
    if task_type == 'Questions':
        show_textbox = "show"

    context = {
        'show_textbox' : show_textbox,
        'adv_id' : adventure_saved,
        'adv_name' : adv_name,
        'task_num' : task_saved,
        'task_detail' : task_detail,
        'task_ans' : task_ans,
        "task_description" : task_description,
    }

    return render(request, 'map/taskpage.html', context)


def mission_task_submission(request):
    """
    This function updates user's current progress of the specific adventure(e.g. a user completes a task).

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject or HttoResponseObjects
        It returns HttoResponseRedirectObjects, it redirects a user to next task when he completes one.
        It returns HttoResponseObjects when a user completes all the tasks in a specific adventure.
    """
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = game_saved.task_saved
    adv = Adventure.objects.get(adventure_id=adventure_saved)
    Current_adventures = current_adventures.objects.filter(user = user)
    current_adventure = Current_adventures.get(adventure_saved = adventure_saved)
    tasks = Task.objects.filter(adventure_name=adv)
    level_number = user.level_num
    if task_saved == str(len(tasks)):
        user.game_saved.task_saved = "1"
        game_saved.save()
        current_adventure.task_saved = game_saved.task_saved
        current_adventure.save()
        level_number.user_point = level_number.user_point + 25
        if level_number.user_point >= 100:
            level_number.user_level = level_number.user_level + 1
            level_number.user_point = level_number.user_point - 100
        level_number.save()
        Track.objects.create(user=user, adventure_done=adventure_saved)
        return render(request, 'map/adventure_completion.html')
    game_saved.task_saved = str(int(game_saved.task_saved) + 1)
    game_saved.save()
    current_adventure.task_saved = game_saved.task_saved
    current_adventure.save()

    level_number.user_point = level_number.user_point + 25
    if level_number.user_point >= 100:
        level_number.user_level = level_number.user_level + 1
        level_number.user_point = level_number.user_point - 100
    level_number.save()
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)
    new_url = 'task' + str(game_saved.task_saved)
    messages.success(request, 'You gain Exp 25 points!')
    return HttpResponseRedirect(new_url)


def questions_task_submission(request):
    """
    This function processes the answers submitted by a user, and takes user to next
    task if user's answer is correct or keeps user in current page when auser's answer
    is wrong.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    HttpResponseRedirectObject or HttoResponseObjects
        It returns HttoResponseRedirectObjects, it redirects a user to next task when he completes one.
        It returns HttoResponseObjects when a user completes all the tasks in a specific adventure.
    """
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = game_saved.task_saved
    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    Current_adventures = current_adventures.objects.filter(user = user)
    current_adventure = Current_adventures.get(adventure_saved = adventure_saved)
    tasks = Task.objects.filter(adventure_name=adv)
    level_number = user.level_num
    if task_saved == str(len(tasks)):
        game_saved.task_saved = "1"
        game_saved.save()
        current_adventure.task_saved = game_saved.task_saved
        current_adventure.save()
        level_number.user_point = level_number.user_point + 25
        if level_number.user_point >= 100:
            level_number.user_level = level_number.user_level + 1
            level_number.user_point = level_number.user_point - 100
        level_number.save()
        Track.objects.create(user=user, adventure_done=adventure_saved)
        return render(request, 'map/adventure_completion.html')
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)
    user_ans = request.GET.get('task_ans','')

    if user_ans:
        task_ans = task.task_ans
        if user_ans == task_ans:
            game_saved.task_saved = str(int(game_saved.task_saved) + 1)
            game_saved.save()
            task_saved = game_saved.task_saved
            current_adventure.task_saved = game_saved.task_saved
            current_adventure.save()

            level_number.user_point = level_number.user_point + 25
            if level_number.user_point >= 100:
                level_number.user_level = level_number.user_level + 1
                level_number.user_point = level_number.user_point - 100
            level_number.save()
            new_url = 'task' + str(task_saved)
            messages.success(request, 'You gain Exp 25 points!')
            return HttpResponseRedirect(new_url)
        else:
            new_url = 'task' + str(task_saved)
            messages.success(request, 'Sorry, the result is incorrect..')
            return HttpResponseRedirect(new_url)

    else:
        new_url = 'task' + str(task_saved)
        messages.warning(request, 'Sorry, textfield is empty')
        return HttpResponseRedirect(new_url)


def special_game_json(request):
    """
    This function pass JSON data to front-end and Javascript in the front-end will
    processes these data and show it to a user.

    Parameters
    ----------
    request: HttpRequestObject
        Django request object that contains a variety of information from the middlewares.

    Returns
    -------
    Application/JSON
        It returns Application/JSON to front-end.
    """
    user = request.user
    game_saved = user.game_saved
    task_saved = game_saved.task_saved
    adventure_saved = game_saved.adventure_saved
    adventure = Adventure.objects.get(adventure_id=adventure_saved)
    task = Task.objects.get(adventure_name=adventure, task_number=task_saved)
    special_game = task.special_game
    alist = {"special_game": special_game}
    return JsonResponse(alist, safe=False)
