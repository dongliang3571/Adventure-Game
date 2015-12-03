from coreapp.models import Character

def islogged(request):
    if not Character.objects.all():
        return {'islogged':''}
    elif Character.objects.filter(is_logged=True):
        return { 'islogged':"True" }
    else:
        return {'islogged':''}
