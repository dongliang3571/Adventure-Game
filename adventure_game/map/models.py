from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.


class Level(models.Model):

    user = models.OneToOneField(User,primary_key=True)
    level_number = models.IntegerField(default=0)
    question_number = models.IntegerField(default=1)
    task1_question1_completion = models.BooleanField(default=False)


    def __unicode__(self):
        return str(self.user.username)+"'s current level is '" + str(self.level_number)

class hint(models.Model):

    hint_text = models.CharField(max_length=200)


    def __unicode__(self):
        return 'Hint is <'+str(self.hint_text)+'>'

class QuestionAndAnswer(models.Model):
    hint = models.ForeignKey(hint)
    Question = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)
    QuestionNumber = models.IntegerField(default=1)
    def __unicode__(self):
        return 'Question #'+str(self.QuestionNumber)+' Question: '+str(self.Question)+'Answer: '+str(self.Answer)

################################################################
class Adventure(models.Model):
    adventure_id = models.CharField(unique=True, max_length=50, default=0000)
    adventure_name = models.CharField(max_length=200)
    adventure_description = models.TextField(max_length=200)

    adventure_category_choices = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    adventure_category = models.CharField(max_length=10, choices = adventure_category_choices, default='Outdoor')

    def __str__(self):
        return self.adventure_name


class Task(models.Model):
    adventure_name = models.ForeignKey(Adventure)
    task = models.CharField(max_length=200)
    task_details = models.TextField(max_length=200)
    hint = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.task

class Hints(models.Model):
    task = models.ForeignKey(Task)
    hints = models.CharField(max_length=200) #answers to the all the questions
    question = models.CharField(max_length=200)

    def __str__(self):
        return self.hint


class Answer(models.Model):
    question = models.ForeignKey(Hints)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return 'Q: '+self.question + 'A: '+self.answer
