from .queries import (load_adventures, load_completed_adventures,
                      load_game_save_id, get_character_name
                     )

def get_profile_context(user, characters):
    adventure_name_list = []
    adventure_img_url_list = []
    adventure_id_list = []
    adventure_complete_list = []

    load_adventures(adventure_name_list, adventure_img_url_list, adventure_id_list)
    load_completed_adventures(adventure_complete_list, user)
    zipped = zip(adventure_img_url_list, adventure_name_list, adventure_id_list)

    level = user.level_num
    game_saved_id_list = []
    load_game_save_id(game_saved_id_list, user)
    character_name = get_character_name(characters)
    context = {'character_name' : character_name,
               'level' : level,
               'game_saved' : game_saved_id_list,
               'zipped' : zipped,
               'completed_list' : adventure_complete_list,
              }
    return context