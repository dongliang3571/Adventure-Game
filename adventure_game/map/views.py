from django.shortcuts import render
from .models import Level
from .models import QuestionAndAnswer
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
    # user = request.user
    #
    # if user.is_authenticated():
    #     if not user.character_set.all():
    #         messages.warning(request, 'Create your family roles so that you can start your adventures.')
    #         return HttpResponseRedirect(reverse('coreapp:profile'))
    #     else:
    #
    #         game_saved = user.game_saved.task_saved
    #         task_saved = int(game_saved)
    #
    #         if task_saved == 1:
    #             boyn = "boy"
    #         elif task_saved == 2:
    #             boyn = "boy boy1"
    #         elif task_saved == 3:
    #             boyn = "boy boy1 boy2"
    #         elif task_saved == 4:
    #             boyn = "boy boy1 boy2 boy3"
    #         elif task_saved == 5:
    #             boyn = "boy boy1 boy2 boy3 boy4"
    #         messages.warning(request, 'Welcome to your adventures')
    #         return render(request, 'map/map.html', {'boyn':boyn})
    # else:
    #     messages.warning(request, 'Please sign in')
    #     return HttpResponseRedirect(reverse('coreapp:home'))
    adventureid = request.GET.get('adventureid', '')
    adv = Adventure.objects.get(adventure_id=adventureid)
    task_list = Task.objects.filter(adventure_name=adv)
    task_num_list = []
    task_name_list = []
    place_img_url_list = []
    task_ans_list = []
    for i in task_list:
        task_num_list.append(i.task_number)
        task_name_list.append(i.task_name)
        place_img_url_list.append(i.place_img_url)
    # task_name_list = Task.task_name.filter(adventure_name=adv)


    context = {'adventureid' : adventureid,
               'task_num1' : task_num_list[0],
               'task_num2' : task_num_list[1],
               'task_num3' : task_num_list[2],
               'task_num4' : task_num_list[3],
               'task_num5' : task_num_list[4],

               'task_name1' : task_name_list[0],
               'task_name2' : task_name_list[1],
               'task_name3' : task_name_list[2],
               'task_name4' : task_name_list[3],
               'task_name5' : task_name_list[4],

               'place_img_url1' : place_img_url_list[0],
               'place_img_url2' : place_img_url_list[1],
               'place_img_url3' : place_img_url_list[2],
               'place_img_url4' : place_img_url_list[3],
               'place_img_url5' : place_img_url_list[4],

    }
    return render(request, 'map/map.html', context)



def beginingstory(request):
    """
    This function takes user to a transmission page that only display once when users first begin the adventure.
    """
    user = request.user
    adventureid = request.GET.get('adventureid', '')
    if Game_saved.objects.filter(user=user):
        return HttpResponseRedirect(reverse('map:map'))
    else:
        game_saved = Game_saved.objects.create(user=user, adventure_saved=adventureid, task_saved='1')
        # task_saved = int(game_saved.task_saved)
        return render(request, 'map/task1.html')


def story(request):
    adventureid = request.GET.get('adventureid', '')
    adv = Adventure.objects.get(adventure_id=adventureid)
    adv_descrip = adv.adventure_description
    context = {'adventureid' : adventureid,
               'adventuredescrip' : adv_descrip,

    }
    return render(request, 'map/story.html', context)



def task(request):
    """
    This functions retrives tasks from database and display on task pages for users to complete.
    """
#     if request.user.is_authenticated():
#         if request.user.level.task1_question1_completion == True:
#             return HttpResponseRedirect(reverse('map:task1_question2'))
#
#         ques = request.GET.get('question', '')
#         ans = request.GET.get('answer', '')
#         questionnumber = request.GET.get('questionNumber', '')
#         if ans:
#             correct_answer = QuestionAndAnswer.objects.get(Question=ques).Answer
#             if ans == correct_answer:
#                 if request.user.level.question_number == 10:
#                     # housenumber = ''
#                     # for n in range(request.user.level.question_number):
#                     #     questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber = n+1)
#                     #     housenumber = housenumber+' '+str(questionTempObject.Answer)
#
#                     hi = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
#                     housenumber = hi.hint_text
#                     user = request.user
#                     le = request.user.level
#                     le.task1_question1_completion = True;
#                     le.save()
#                     return render(
#                         request, 'map/task1_question1.html', {
#                             'isShow':'show', 'houseNumber':housenumber,
#                             'message':'Congradulations, You have gotten your clue.', 'isComplete':'complete'})
#                 user = request.user
#                 le = request.user.level
#                 # l.level_number = l.level_number+1
#                 le.question_number = le.question_number+1
#                 le.save()
#                 questionNumber = le.question_number
#                 questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
#                 question = questionObject.Question
#
#                 housenumber = ''
#                 for n in range(questionNumber-1):
#                     questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
#                     housenumber = housenumber+' '+str(questionTempObject.Answer)
#
#                 return render(
#                     request, 'map/task1_question1.html', {
#                         'message':'Your answer is correct, keep going.',
#                         'isShow':'show', 'question':question, 'houseNumber':housenumber})
#             else:
#                 user = request.user
#                 questionNumber = user.level.question_number
#                 questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
#                 question = questionObject.Question
#                 housenumber = ''
#                 for n in range(questionNumber-1):
#                     questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
#                     housenumber = housenumber+' '+str(questionTempObject.Answer)
#                 return render(
#                     request, 'map/task1_question1.html', {
#                         'message2':'Sorry, Your answer is Wrong, Try again....',
#                         'isShow':'show', 'question':question, 'houseNumber':housenumber})
#         else:
#             user = request.user
#             questionNumber = user.level.question_number
#             questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
#             question = questionObject.Question
#             housenumber = ''
#             for n in range(questionNumber-1):
#                 questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
#                 housenumber = housenumber+' '+str(questionTempObject.Answer)
#             return render(
#                 request, 'map/task1_question1.html', {
#                     'isShow':'show', 'question':question,
#                     'houseNumber':housenumber})
#     else:
#         messages.warning(request, 'Please sign in.')
#         return HttpResponseRedirect(reverse('coreapp:home'))

    user = request.user

    adv = Adventure.objects.get(adventure_id="0000") #needed to get from adv
    task_num = 1    #needed to get from map

    #saving game
    game_saved_adv = adv
    game_saved_task = task_num

    task = Task.objects.get(adventure_name=adv, task_number=task_num)
    task_detail = task.task_detail
    task_ans = task.task_ans

    context = {'adv_name' : adv,
               'task_num' : task_num,
               'task_detail' : task_detail,
               'task_ans' : task_ans,
    }
    return render(request, 'map/taskpage.html', context)

def Task_Submission(request):
    adv = Adventure.objects.get(adventure_id="0000")
    task_num = 1
    task = Task.objects.get(adventure_name=adv, task_number=task_num)
    task_detail = task.task_detail
    task_ans = task.task_ans

    user_ans = request.POST.get('task_ans','')

    context = {'adv_name' : adv,
               'task_num' : task_num,
               'task_detail' : task_detail,
               'task_ans' : task_ans,
    }
    if user_ans == task.task_ans:
        task_num = task_num+1
        task = Task.objects.get(adventure_name=adv, task_number=task_num)
        task_detail = task.task_detail
        task_ans = task.task_ans

        context = {'adv_name' : adv,
                   'task_num' : task_num,
                   'task_detail' : task_detail,
                   'task_ans' : task_ans,
        }
        return render(request, 'map/taskpage.html', context)
    else:
        messages.success(request, 'Sorry, the result is incorrect..')
        return render(request, 'map/taskpage.html', context)



def task1_question2(request):
    h = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
    housenumber = h.hint_text
    return render(request, 'map/task1_question2.html', {'houseNumber':housenumber})

def task2(request):
    return render(request, 'map/task2.html')
