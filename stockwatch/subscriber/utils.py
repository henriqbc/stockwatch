from . import models
from django.core.exceptions import ObjectDoesNotExist

class AuthenticationError(Exception):
    def __init__(self, message="User is not authenticated"):
        self.message = message
        super().__init__(self.message)

def get_username() -> str:
    try:
        user = models.UserModel.objects.get(id=1)
        username = user.name
    except ObjectDoesNotExist:
        raise AuthenticationError
    
    return username

def get_user_email() -> str:
    try:
        user = models.UserModel.objects.get(id=1)
        user_email = user.email
    except ObjectDoesNotExist:
        raise AuthenticationError
    
    return user_email

def get_user_info() -> list[str, str]:
    try:
        user = models.UserModel.objects.get(id=1)
        username = user.name
        user_email = user.email
    except ObjectDoesNotExist:
        raise AuthenticationError
    
    return username, user_email