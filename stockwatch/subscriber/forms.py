from django import forms
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field ff-text', 'max_lenght': str(models.MAX_STR_FIELD_SIZE)}),
            'email': forms.EmailInput(attrs={'class': 'form-field ff-text'}),
        }