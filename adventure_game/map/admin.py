from django.contrib import admin
from .models import Level
from .models import QuestionAndAnswer
# Register your models here.

admin.site.register(Level)
admin.site.register(QuestionAndAnswer)

##########################################
from .models import Adventure, Task, Hints

class HintsInLine(admin.StackedInline):
    model = Hints
    extra = 3

class TaskInLine(admin.StackedInline):
    model = Task
    extra = 3

class AdventureAdmin(admin.ModelAdmin):
    inlines = [TaskInLine]
    list_display = ('adventure_id', 'adventure_name', 'adventure_category')
    ordering = ['adventure_id']
admin.site.register(Adventure, AdventureAdmin)
