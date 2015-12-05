from coreapp.models import Character

def islogged(request):
    user = request.user
    if user.is_authenticated():

        chars = user.character_set.filter(is_logged=True)
        if chars:
            char = user.character_set.get(is_logged=True)
            char_name = char.character_name
            return {'islogged':char_name}
        else:
            return {'islogged':''}
    else:
        return {'islogged':''}
