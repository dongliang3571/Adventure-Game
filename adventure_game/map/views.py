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
    user = request.user
    adventureid = request.GET.get('adventureid', '')
    if user.is_authenticated():
        if not user.character_set.all():
            messages.warning(request, 'Create your family roles so that you can start your adventures.')
            return HttpResponseRedirect(reverse('coreapp:profile'))
        else:

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
        messages.warning(request, 'Please sign in')
        return HttpResponseRedirect(reverse('coreapp:home'))



def task1_question1(request):
    if request.user.is_authenticated():
        if request.user.level.task1_question1_completion == True:
            return HttpResponseRedirect(reverse('map:task1_question2'))

        ques = request.GET.get('question', '')
        ans = request.GET.get('answer', '')
        questionnumber = request.GET.get('questionNumber', '')
        if ans:
            correct_answer = QuestionAndAnswer.objects.get(Question=ques).Answer
            if ans == correct_answer:
                if request.user.level.question_number == 10:
                    # housenumber = ''
                    # for n in range(request.user.level.question_number):
                    #     questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber = n+1)
                    #     housenumber = housenumber+' '+str(questionTempObject.Answer)

                    hi = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
                    housenumber = hi.hint_text
                    user = request.user
                    le = request.user.level
                    le.task1_question1_completion = True;
                    le.save()
                    return render(
                        request, 'map/task1_question1.html', {
                            'isShow':'show', 'houseNumber':housenumber,
                            'message':'Congradulations, You have gotten your clue.', 'isComplete':'complete'})
                user = request.user
                le = request.user.level
                # l.level_number = l.level_number+1
                le.question_number = le.question_number+1
                le.save()
                questionNumber = le.question_number
                questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
                question = questionObject.Question

                housenumber = ''
                for n in range(questionNumber-1):
                    questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                    housenumber = housenumber+' '+str(questionTempObject.Answer)

                return render(
                    request, 'map/task1_question1.html', {
                        'message':'Your answer is correct, keep going.',
                        'isShow':'show', 'question':question, 'houseNumber':housenumber})
            else:
                user = request.user
                questionNumber = user.level.question_number
                questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
                question = questionObject.Question
                housenumber = ''
                for n in range(questionNumber-1):
                    questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                    housenumber = housenumber+' '+str(questionTempObject.Answer)
                return render(
                    request, 'map/task1_question1.html', {
                        'message2':'Sorry, Your answer is Wrong, Try again....',
                        'isShow':'show', 'question':question, 'houseNumber':housenumber})
        else:
            user = request.user
            questionNumber = user.level.question_number
            questionObject = QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
            question = questionObject.Question
            housenumber = ''
            for n in range(questionNumber-1):
                questionTempObject = QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                housenumber = housenumber+' '+str(questionTempObject.Answer)
            return render(
                request, 'map/task1_question1.html', {
                    'isShow':'show', 'question':question,
                    'houseNumber':housenumber})
    else:
        messages.warning(request, 'Please sign in.')
        return HttpResponseRedirect(reverse('coreapp:home'))


def task1_question2(request):
    h = QuestionAndAnswer.objects.get(QuestionNumber=10).hint
    housenumber = h.hint_text
    return render(request, 'map/task1_question2.html', {'houseNumber':housenumber})

def task2(request):
    return render(request, 'map/task2.html')
