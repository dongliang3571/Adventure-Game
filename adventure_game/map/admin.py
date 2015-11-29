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

admin.site.register(Adventure, AdventureAdmin)
