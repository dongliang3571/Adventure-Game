from map.models import Adventure
from .models import Track, Game_saved

def load_adventures(adventure_name_list, adventure_img_url_list, adventure_id_list):
    for i in Adventure.objects.all():
        adventure_name_list.append(str(i.adventure_name))
        adventure_img_url_list.append(str(i.adventure_img_url))
        adventure_id_list.append(str(i.adventure_id))

def load_completed_adventures(adventure_complete_list, user):
    for n in Track.objects.filter(user=user):
        adventure_complete_list.append(str(n.adventure_done))

def is_character_logged_in(characters):
    return characters.filter(is_logged=True)

def load_game_save_id(game_saved_id_list, user):
    if Game_saved.objects.filter(user=user):
        for game_saved in Game_saved.objects.filter(user=user):
            game_saved_id_list.append(str(game_saved.adventure_saved))

def get_character_name(characters):
    return characters.filter(is_logged=True)[0].character_name

#Temp note, returns list of character models
def get_all_characters(user):
    return user.character_set.all()
