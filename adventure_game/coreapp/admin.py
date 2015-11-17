from django.contrib import admin
from .models import UserProfile, character

# Register your models here.
admin.site.register(UserProfile, character)
