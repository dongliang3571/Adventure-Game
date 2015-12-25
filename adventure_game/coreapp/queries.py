""" This module contains functions that perform queries to the database.
"""
from map.models import Adventure
from .models import Track, Game_saved

def load_adventures(adventure_name_list, adventure_img_url_list,
                    adventure_id_list, adventure_description_list):
    """This function populates the arguments with information about the
    adventure.

    Parameters
    ---------
    adventure_name_list: list
        List that holds the adventure names.

    adventure_img_url_list: list
        List that holds the image urls.

    adventure_id_list: list
        List that holds the adventure IDs.

    adventure_description_list: list
        List that holds the descriptions
    """
    for i in Adventure.objects.all():
        adventure_name_list.append(str(i.adventure_name))
        adventure_img_url_list.append(str(i.adventure_img_url))
        adventure_id_list.append(str(i.adventure_id))
        adventure_description_list.append(i.adventure_description)

def load_completed_adventures(adventure_complete_list, user):
    """This function populates a list with information about what
    adventures the user has completed.

    Parameters
    ----------
    adventure_complete_list: List
        List that holds the information about completed adventures.

    user: User
        The user model for currently logged in user.
    """
    for i in Track.objects.filter(user=user):
        adventure_complete_list.append(str(i.adventure_done))

def get_logged_in_char(characters):
    """This function queries the database for the logged in family member
    and returns it.

    Parameters
    ----------
    characters: List
        List of Character models associated with the logged in user.

    Returns
    -------
    Character
        Returns the character model representhing the logged in family member.
    """
    return characters.filter(is_logged=True)

def load_game_save_id(game_saved_id_list, user):
    """This function queries the database for game save ids and
    populates the list passed in.

    Parameters
    ----------
    game_save_id_list: List
        List that holds the Game saved IDs

    user: User
        User model representing the logged in User.
    """
    if Game_saved.objects.filter(user=user):
        for game_saved in Game_saved.objects.filter(user=user):
            game_saved_id_list.append(str(game_saved.adventure_saved))

def get_character_name(characters):
    """This function queries the database for the name of the logged in
    family member.

    Parameters
    ----------
    characters: List
        List of Character models associated with the logged in user.

    Returns
    -------
    String
        Returns the name of the loged in family member.
    """
    return characters.filter(is_logged=True)[0].character_name

#Temp note, returns list of character models
def get_all_characters(user):
    """This function returns the list of family members associated
    with the account.

    Parameters
    ----------
    user: User
        User model of the logged in user.

    Returns
    -------
    List
        List of Character models that represent the family members associated
        with the account.
    """
    return user.character_set.all()
