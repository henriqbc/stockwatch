from .models import UserModel
from django.core.exceptions import ObjectDoesNotExist

def username_variable(request):
    try:
        user = UserModel.objects.get(id=1)
        username = user.name
    except ObjectDoesNotExist:
        username = 'User'

    return {'username': username}