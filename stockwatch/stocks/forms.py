from django import forms
from . import models
    
class RegisterStock(forms.ModelForm):
    name = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-field dropdown'}))

    def __init__(self, *args, choices=None, **kwargs):
        super(RegisterStock, self).__init__(*args, **kwargs)
        if choices:
            self.fields['name'].choices = choices

    class Meta:
        model = models.MonitoredStock
        fields = ['name', 'upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']
        widgets = {
            'upper_tunnel_bound': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
            'lower_tunnel_bound': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
            'periodicity': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
        }

class UpdateStock(forms.ModelForm):
    class Meta:
        model = models.MonitoredStock
        fields = ['upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']
        widgets = {
            'upper_tunnel_bound': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
            'lower_tunnel_bound': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
            'periodicity': forms.NumberInput(attrs={'class': 'form-field ff-number'}),
        }