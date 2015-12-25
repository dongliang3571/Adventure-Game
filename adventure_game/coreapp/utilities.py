from .queries import (load_adventures, load_completed_adventures,
                      load_game_save_id, get_character_name
                     )
from map.models import Adventure
from .models import current_adventures, Track

def get_profile_context(user, characters):
    adventure_name_list = []
    adventure_img_url_list = []
    adventure_id_list = []
    adventure_complete_list = []
    adventure_description_list = []
    adventure_is_playing = [] #newly added
    adventure_has_played = [] #newly added

    adventures = Adventure.objects.all()
    Current_adventures = current_adventures.objects.filter(user=user).order_by("id")
    tracks = Track.objects.filter(user=user).order_by("id")
    for adventure in adventures:
        is_playing = Current_adventures.filter(adventure_saved=adventure.adventure_id)
        if is_playing:
            adventure_is_playing.append("is_playing")
        else:
            adventure_is_playing.append("")
        has_played = tracks.filter(adventure_done=adventure.adventure_id)
        if has_played:
            adventure_has_played.append("has_played")
        else:
            adventure_has_played.append("")

    load_adventures(adventure_name_list, adventure_img_url_list, adventure_id_list, adventure_description_list)
    load_completed_adventures(adventure_complete_list, user)
    zipped = zip(adventure_img_url_list, adventure_name_list, adventure_id_list, adventure_description_list, adventure_is_playing, adventure_has_played)

    level = int(user.level_num.user_level)
    exp = user.level_num.user_point
    game_saved_id_list = []
    load_game_save_id(game_saved_id_list, user)
    character_name = get_character_name(characters)
    context = {'character_name' : character_name,
               'level' : level,
               'game_saved' : game_saved_id_list,
               'zipped' : zipped,
               'completed_list' : adventure_complete_list,
               'exp' : exp,
               'rangelist' : range(level)
              }
    return context

def get_adventure_info(): #for home page, displays adv info
        adventure_name_list = []
        adventure_img_url_list = []
        adventure_id_list = []
        adventure_description_list = []

        load_adventures(adventure_name_list, adventure_img_url_list, adventure_id_list, adventure_description_list)
        zipped = zip(adventure_img_url_list, adventure_name_list, adventure_id_list, adventure_description_list)

        context = {
            'zipped' : zipped,
        }
        return context
