from subscriber.models import UserModel
from django.core.exceptions import ObjectDoesNotExist

NOT_SUSCRIBED = 1

def username_variable(request):
    try:
        user = UserModel.objects.get(id=1)
        username = user.name
    except ObjectDoesNotExist:
        username = 'User'

    return {'username': username}

def global_username():
    try:
        user = UserModel.objects.get(id=1)
        username = user.name
    except ObjectDoesNotExist:
        return NOT_SUSCRIBED

    return username