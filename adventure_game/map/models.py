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
    adventure_id = models.CharField(unique=True, max_length=50, default='0000')
    adventure_name = models.CharField(max_length=200)
    adventure_description = models.TextField(max_length=200, blank=True, default='')

    adventure_category_choices = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    adventure_category = models.CharField(max_length=10, choices = adventure_category_choices, default='Outdoor')

    def __unicode__(self):
        return self.adventure_name


class Task(models.Model):
    adventure_name = models.ForeignKey(Adventure)
    task_num_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    task_number = models.CharField(max_length=10, choices = task_num_choices, default='1')
    task_type_choices = (
        ('Mission', 'Mission'),
        ('Questions', 'Questions'),
    )
    task_type = models.CharField(max_length=10, choices = task_type_choices, default='Mission')
    task_detail = models.TextField(max_length=200, blank=True, default='')
    place_img_url = models.URLField(blank=True, default='')
    hint = models.CharField(max_length=200, blank=True, default='')
    def __unicode__(self):
        return self.task_number

class Question(models.Model):
    question_type_choices = (
        ('Math', 'Math'),
        ('English', 'English'),
        ('History', 'History'),
        ('Science', 'Science'),
    )
    question_type = models.CharField(max_length=10, choices = question_type_choices, default='Math')
    question_age_choices = (
        ('1. Pre-k', 'Pre-k'),
        ('2. Age 4-7', 'Age 4-7'),
        ('3. Age 8-10', 'Age 8-10'),    #index is for ordering
    )
    question_age = models.CharField(max_length=20, choices = question_age_choices, default='Pre-k')
    question_text = models.TextField(max_length=200, blank=True, default='')
    def __unicode__(self):
        return self.question_text

class Answer(models.Model):
    question_text = models.OneToOneField(Question)
    choice_1 = models.CharField(max_length=200, blank=True, default='')
    choice_2 = models.CharField(max_length=200, blank=True, default='')
    choice_3 = models.CharField(max_length=200, blank=True, default='')
    choice_4 = models.CharField(max_length=200, blank=True, default='')
    answer_choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', 'None from above'),
    )
    answer = models.CharField(max_length=10, choices = answer_choices, default='5')

    def __unicode__(self):
        return 'Q: '+str(self.question_text) + 'A: '+str(self.answer)
