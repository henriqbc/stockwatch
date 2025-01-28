from django import forms
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['name', 'email']