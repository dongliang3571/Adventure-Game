from django.shortcuts import render
from .models import Level
from .models import QuestionAndAnswer
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
# Create your views here.

def index(request):
    user=request.user
    if user.is_authenticated():
        if user.is_superuser==True:
            messages.warning(request, 'Please login as a regular user to enter the map rather than a super user')
            return HttpResponseRedirect(reverse('coreapp:home'))
        else:

            ln=user.level.level_number

            if ln==0:
                boyn="boy"
            elif ln==1:
                boyn="boy boy1"
            elif ln==2:
                boyn="boy boy1 boy2"
            elif ln==3:
                boyn="boy boy1 boy2 boy3"
            elif ln==4:
                boyn="boy boy1 boy2 boy3 boy4"
            messages.warning(request, 'Welcome to your adventures')
            return render(request, 'map/index.html',{'boyn':boyn})
    else:
        messages.warning(request, 'Please sign in')
        return HttpResponseRedirect(reverse('coreapp:home'))

def task1(request):
    return render(request,'map/task1.html')

def task1_question1(request):
    if request.user.is_authenticated():
        if request.user.level.task1_question1_completion==True:
            return HttpResponseRedirect(reverse('map:task1_question2'))
    # if request.user.level.question_number==11:
    #     housenumber='888 Madision ave, New York, NY10021'
    #     return render(request, 'map/task1_question1.html', {'message':'Congradulations, You have gotten your clue.','isComplete':'complete','houseNumber':housenumber})
        ques = request.GET.get('question','')
        ans = request.GET.get('answer','')
        questionnumber = request.GET.get('questionNumber','')
        if ans:
            correct_answer = QuestionAndAnswer.objects.get(Question=ques).Answer
            if ans==correct_answer:
                if request.user.level.question_number==10:
                    # housenumber=''
                    # for n in range(request.user.level.question_number):
                    #     questionTempObject=QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                    #     housenumber=housenumber+' '+str(questionTempObject.Answer)

                    housenumber='888 Madision ave, New York, NY 10021'
                    user=request.user
                    l = request.user.level
                    l.task1_question1_completion = True;
                    l.save()
                    return render(request, 'map/task1_question1.html',{'isShow':'show','houseNumber':housenumber,
                    'message':'Congradulations, You have gotten your clue.','isComplete':'complete'})
                user=request.user
                l = request.user.level
                # l.level_number=l.level_number+1
                l.question_number=l.question_number+1
                l.save()
                questionNumber=l.question_number
                questionObject=QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
                question=questionObject.Question

                housenumber=''
                for n in range(questionNumber-1):
                    questionTempObject=QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                    housenumber=housenumber+' '+str(questionTempObject.Answer)

                # if questionNumber==11:
                #     # housenumber='888 Madision ave, New York, NY10021'
                #     # return render(request, 'map/task1_question1.html', {'message':'Congradulations, You have gotten your clue.','isComplete':'complete','houseNumber':housenumber})
                #     return render(request, 'map/task1_question1.html',{'message':'Congradulations, You have gotten your clue.','isComplete':'complete',
                #     'isShow':'show','houseNumber':housenumber})
                return render(request, 'map/task1_question1.html',{'message':'Your answer is correct, keep going.',
                'isShow':'show','question':question,'houseNumber':housenumber})
            else:
                user=request.user
                questionNumber=user.level.question_number
                questionObject=QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
                question=questionObject.Question
                housenumber=''
                for n in range(questionNumber-1):
                    questionTempObject=QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                    housenumber=housenumber+' '+str(questionTempObject.Answer)
                return render(request, 'map/task1_question1.html',{'message2':'Sorry, Your answer is Wrong, Try again....',
                'isShow':'show','question':question,'houseNumber':housenumber})
        else:
            user=request.user
            questionNumber=user.level.question_number
            questionObject=QuestionAndAnswer.objects.get(QuestionNumber=questionNumber)
            question=questionObject.Question
            housenumber=''
            for n in range(questionNumber-1):
                questionTempObject=QuestionAndAnswer.objects.get(QuestionNumber=n+1)
                housenumber=housenumber+' '+str(questionTempObject.Answer)
            return render(request, 'map/task1_question1.html',{'isShow':'show','question':question,'houseNumber':housenumber})
    else:
        messages.warning(request,'Please sign in.')
        return HttpResponseRedirect(reverse('coreapp:home'))


def task1_question2(request):
    return render(request, 'map/task1_question2.html')

def task2(request):
    return render(request,'map/task2.html')
