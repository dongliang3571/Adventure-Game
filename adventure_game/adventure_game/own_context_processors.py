from coreapp.models import Character

def islogged(request):
    if not Character.objects.all():
        return {'islogged':''}
    elif Character.objects.filter(user=request.user, is_logged=True):
        char = Character.objects.filter(user=request.user, is_logged=True)[0]
        character_name = str(char.character_name)
        return { 'islogged': character_name}
    else:
        return {'islogged':''}
