from django.contrib import admin
from .models import Level
from .models import QuestionAndAnswer
# Register your models here.

admin.site.register(Level)
# admin.site.register(QuestionAndAnswer)

##########################################
from .models import Adventure, Task, Question, Answer


class TaskInLine(admin.StackedInline):
    model = Task
    ordering = ['task_number']
    # fieldsets = [
    #     (None,               {'fields': ['task_detail']}),
    #     (None,               {'fields': ['hint'], 'classes': ['collapse']}),
    # ]
    extra = 1

class AdventureAdmin(admin.ModelAdmin):
    inlines = [TaskInLine]
    list_display = ('adventure_name', 'adventure_id', 'adventure_category')
    ordering = ['adventure_id']

    fieldsets = [
        (None,               {'fields': ['adventure_id']}),
        (None,               {'fields': ['adventure_name']}),
        (None,               {'fields': ['adventure_category']}),
        (None,               {'fields': ['adventure_img_url']}),
        ('Description',      {'fields': ['adventure_description'], 'classes': ['collapse']}),
    ]


class AnswerInLine(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]
    list_display = ('question_text', 'question_age', 'question_type')
    ordering = ['question_age']

admin.site.register(Adventure, AdventureAdmin)
admin.site.register(Question, QuestionAdmin)
