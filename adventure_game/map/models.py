from django.db import models
from django.contrib import auth
from django.contrib.auth.models import User
# Create your models here.


class Adventure(models.Model):
    """
    This holds our adventure game
    """
    adventure_id = models.CharField(unique=True, max_length=50, default='0000')
    adventure_name = models.CharField(max_length=200)
    adventure_description = models.TextField(max_length=200, blank=True, default='')
    adventure_img_url = models.URLField(blank=True, default='')

    adventure_category_choices = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    adventure_category = models.CharField(max_length=10, choices = adventure_category_choices, default='Outdoor')

    def __unicode__(self):
        return self.adventure_name


class Task(models.Model):
    """
    This holds the tasks of each adventure game.
    """
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
    task_ans = models.CharField(max_length=200, blank=True, default='')
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
