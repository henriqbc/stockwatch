from .models import UserModel
from django.core.exceptions import ObjectDoesNotExist
from . import utils

def username_variable(request):
    try:
        user = UserModel.objects.get(id=1)
        username = user.name
    except ObjectDoesNotExist:
        username = 'User'

    return {'username': username}

def user_registered_variable(request):
    try:
        utils.get_username()
    except utils.AuthenticationError:
        return {'user_authenticated': False}
    
    return {'user_authenticated': True}