from django import forms
from . import models

class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserModel
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'