from django.contrib import admin
from .models import Level
from .models import QuestionAndAnswer
# Register your models here.

admin.site.register(Level)
admin.site.register(QuestionAndAnswer)

##########################################
from .models import Adventure, Task, Question

# class HintsInLine(admin.StackedInline):
#     model = Hints
#     extra = 3

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
    list_display = ('adventure_id', 'adventure_name', 'adventure_category')
    ordering = ['adventure_id']

    fieldsets = [
        (None,               {'fields': ['adventure_id']}),
        (None,               {'fields': ['adventure_name']}),
        (None,               {'fields': ['adventure_category']}),
        ('Description',      {'fields': ['adventure_description'], 'classes': ['collapse']}),
    ]
admin.site.register(Adventure, AdventureAdmin)
