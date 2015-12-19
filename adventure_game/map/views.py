from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Adventure
from .models import Task
from .models import Question
from .models import Answer
from coreapp.models import Level_num
from coreapp.models import Track
from coreapp.models import Game_saved


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

                game_saved = user.game_saved.task_saved
                task_saved = int(game_saved)

                if task_saved == 1:
                    boyn = "boy"
                elif task_saved == 2:
                    boyn = "boy boy1"
                elif task_saved == 3:
                    boyn = "boy boy1 boy2"
                elif task_saved == 4:
                    boyn = "boy boy1 boy2 boy3"
                elif task_saved == 5:
                    boyn = "boy boy1 boy2 boy3 boy4"
                messages.warning(request, 'Welcome to your adventures')
                return render(request, 'map/map.html', {'boyn':boyn})
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
    # if user.game_saved.adventure_saved:
    #     return HttpResponseRedirect(reverse('map:map'))
    # else:
    #
    game_saved = user.game_saved
    game_saved.adventure_saved = adventureid
    game_saved.task_saved = '1'
    game_saved.save()
    return render(request, 'map/task1.html')

def task(request):
    """
    This function retrives tasks from database and displays on task pages for users to complete.
    """

    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = int(game_saved.task_saved)
    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)

    task_detail = task.task_detail
    task_ans = task.task_ans
    task_type = str(task.task_type)
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
    }

    return render(request, 'map/taskpage.html', context)

    #     user = request.user
    #
    #
    # adv = Adventure.objects.get(adventure_id="0000") #needed to get from adv
    # task_num = 1    #needed to get from map
    #
    # #saving game
    # game_saved_adv = adv
    # game_saved_task = task_num
    #
    # task = Task.objects.get(adventure_name=adv, task_number=task_num)
    # task_detail = task.task_detail
    # task_ans = task.task_ans
    #
    # context = {'adv_name' : adv,
    #            'task_num' : task_num,
    #            'task_detail' : task_detail,
    #            'task_ans' : task_ans,
    # }
    # return render(request, 'map/taskpage.html', context)

def mission_task_submission(request):
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = int(game_saved.task_saved)
    if task_saved == 5:
        Track.objects.create(user=user, adventure_done=adventure_saved)
        return render(request, 'map/adventure_completion.html')
    game_saved.task_saved = str(int(game_saved.task_saved) + 1)
    game_saved.save()

    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)
    new_url = 'task' + str(task_saved)
    return HttpResponseRedirect(new_url)


def questions_task_submission(request):
    user = request.user
    game_saved = user.game_saved
    adventure_saved = str(game_saved.adventure_saved)
    task_saved = int(game_saved.task_saved)
    if task_saved == 5:
        Track.objects.create(user=user, adventure_done=adventure_saved)
        return render(request, 'map/adventure_completion.html')
    adv = Adventure.objects.get(adventure_id=adventure_saved) #needed to get from adv
    adv_name = adv.adventure_name
    task = adv.task_set.get(adventure_name=adv, task_number=task_saved)
    user_ans = request.GET.get('task_ans','')

    if user_ans:
        task_ans = task.task_ans
        if user_ans == task_ans:
            game_saved.task_saved = str(int(game_saved.task_saved) + 1)
            game_saved.save()
            task_saved = game_saved.task_saved
            new_url = 'task' + str(task_saved)
            return HttpResponseRedirect(new_url)
        else:
            new_url = 'task' + str(task_saved)
            messages.success(request, 'Sorry, the result is incorrect..')
            return HttpResponseRedirect(new_url)

    else:
        new_url = 'task' + str(task_saved)
        messages.warning(request, 'Sorry, textfield is empty')
        return HttpResponseRedirect(new_url)

    # adv = Adventure.objects.get(adventure_id="0000")
    # task_num = 1
    # task = Task.objects.get(adventure_name=adv, task_number=task_num)
    # task_detail = task.task_detail
    # task_ans = task.task_ans
    #
    # user_ans = request.POST.get('task_ans','')
    #
    # context = {'adv_name' : adv,
    #            'task_num' : task_num,
    #            'task_detail' : task_detail,
    #            'task_ans' : task_ans,
    # }
    # if user_ans == task.task_ans:
    #     task_num = task_num+1
    #     task = Task.objects.get(adventure_name=adv, task_number=task_num)
    #     task_detail = task.task_detail
    #     task_ans = task.task_ans
    #
    #     context = {'adv_name' : adv,
    #                'task_num' : task_num,
    #                'task_detail' : task_detail,
    #                'task_ans' : task_ans,
    #     }
    #     return render(request, 'map/taskpage.html', context)
    # else:
    #     messages.success(request, 'Sorry, the result is incorrect..')
    #     return render(request, 'map/taskpage.html', context)


def task1_question2(request):
    h = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
    housenumber = h.hint_text
    return render(request, 'map/task1_question2.html', {'houseNumber':housenumber})

def task2(request):
    return render(request, 'map/task2.html')

def scram(request):
    return render(request, 'map/scramble.html')
