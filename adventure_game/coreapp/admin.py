from django.contrib import admin
from .models import UserProfile, PIN

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(PIN)
