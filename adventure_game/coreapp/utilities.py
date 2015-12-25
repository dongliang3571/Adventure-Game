"""This module contains a bunch of utility functions used by the views.
This is to minimize the amount of code inside views.
"""
from .queries import (load_adventures, load_completed_adventures,
                      load_game_save_id, get_character_name
                     )

def get_profile_context(user, characters):
    """This function makes queries to the database to get information about
    the adventures and returns a dictionary with the information.

    Parameters
    ----------
    user: User Object
        The current logged in user.

    characters: List
        A list of Character models.

    Returns
    -------
    context: Dictionary
        Returns a dictionary container character name, level number,
        game save data, adventure information, experience, and
        rangelist.
    """
    adventure_name_list = []
    adventure_img_url_list = []
    adventure_id_list = []
    adventure_complete_list = []
    adventure_description_list = []

    load_adventures(adventure_name_list, adventure_img_url_list,
                    adventure_id_list, adventure_description_list)
    load_completed_adventures(adventure_complete_list, user)
    zipped = zip(adventure_img_url_list, adventure_name_list,
                 adventure_id_list, adventure_description_list)

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
    """This is a utility function that returns a dictionary containing level information

    Returns
    -------
        context: Dictionary
            A dictionary with the key 'zipped' who's value is a list which contains
            adventure name, list of image urls, ID, and description of the adventure.
    """
    adventure_name_list = []
    adventure_img_url_list = []
    adventure_id_list = []
    adventure_description_list = []

    load_adventures(adventure_name_list, adventure_img_url_list,
                    adventure_id_list, adventure_description_list)
    zipped = zip(adventure_img_url_list, adventure_name_list,
                 adventure_id_list, adventure_description_list)

    context = {
        'zipped' : zipped,
    }
    return context
