from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Character, Level_num, Track, Game_saved, ContactUs


admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class CharacterInline(admin.TabularInline):
    model = Character
    extra = 3

class LevelInline(admin.StackedInline):
    model = Level_num

class TrackInLine(admin.StackedInline):
    model = Track
    extra = 1

class Game_savedInLine(admin.TabularInline):
    model = Game_saved

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, CharacterInline, LevelInline, TrackInLine, Game_savedInLine]

admin.site.register(User, UserProfileAdmin)
admin.site.register(ContactUs)
