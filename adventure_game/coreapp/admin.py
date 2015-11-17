from django.contrib import admin
from .models import UserProfile, PIN

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,	{'fields': ['user']}),
	]

admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(PIN)
