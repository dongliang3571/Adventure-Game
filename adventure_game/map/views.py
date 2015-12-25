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
    This function renders entire map where users can see their adventures progress
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
    This function takes user to a transmission page that only displays once when users first begin the adventure.
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
                "adventureid" : adventureid
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
            "adventureid" : adventureid
        }

        return render(request, 'map/details.html',context)

def visitorview(request):
    adventureid = request.GET.get('adventureid', '')

    adventure = Adventure.objects.get(adventure_id = adventureid)
    Adventures_info = adventures_info.objects.get(adventure_name = adventure)
    context = {
        "adventure_title" : adventure.adventure_name,
        "items_needed" : Adventures_info.items_needed,
        "expenses" : Adventures_info.expenses,
        "locations" : Adventures_info.locations,
        "map_address" : Adventures_info.map_address,
        "adventureid" : adventureid
    }

    return render(request, 'map/visitorview.html',context)


def save_current(request):
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
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = game_saved.task_saved
    adv = Adventure.objects.get(adventure_id=adventure_saved)
    Current_adventures = current_adventures.objects.filter(user = user)
    current_adventure = Current_adventures.get(adventure_saved = adventure_saved)
    tasks = Task.objects.filter(adventure_name=adv)
    if task_saved == str(len(tasks)):
        user.game_saved.task_saved = "1"
        game_saved.save()
        current_adventure.task_saved = game_saved.task_saved
        current_adventure.save()
        Track.objects.create(user=user, adventure_done=adventure_saved)
        return render(request, 'map/adventure_completion.html')
    game_saved.task_saved = str(int(game_saved.task_saved) + 1)
    game_saved.save()
    current_adventure.task_saved = game_saved.task_saved
    current_adventure.save()
    level_number = user.level_num
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
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = game_saved.task_saved
    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    Current_adventures = current_adventures.objects.filter(user = user)
    current_adventure = Current_adventures.get(adventure_saved = adventure_saved)
    tasks = Task.objects.filter(adventure_name=adv)
    if task_saved == str(len(tasks)):
        game_saved.task_saved = "1"
        game_saved.save()
        current_adventure.task_saved = game_saved.task_saved
        current_adventure.save()
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
            level_number = user.level_num
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



def task1_question2(request):
    h = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
    housenumber = h.hint_text
    return render(request, 'map/task1_question2.html', {'houseNumber':housenumber})

def task2(request):
    return render(request, 'map/task2.html')

def special_game_json(request):
    user = request.user
    game_saved = user.game_saved
    task_saved = game_saved.task_saved
    adventure_saved = game_saved.adventure_saved
    adventure = Adventure.objects.get(adventure_id=adventure_saved)
    task = Task.objects.get(adventure_name=adventure, task_number=task_saved)
    special_game = task.special_game
    alist = {"special_game": special_game}
    return JsonResponse(alist, safe=False)
