from django import forms
from . import models
    
class RegisterStock(forms.ModelForm):
    class Meta:
        model = models.MonitoredStock
        fields = ['name', 'upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']

class UpdateStock(forms.ModelForm):
    class Meta:
        model = models.MonitoredStock
        fields = ['upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']