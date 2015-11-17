from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Character, PIN


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CharacterInline(admin.TabularInline):
    model = Character
    extra = 4

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, CharacterInline]

admin.site.register(User, UserProfileAdmin)
