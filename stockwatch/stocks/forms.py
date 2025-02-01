from django import forms
from . import models
    
class RegisterStock(forms.ModelForm):
    class Meta:
        model = models.MonitoredStock
        fields = ['name', 'upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']
    
    def __init__(self, *args, **kwargs):
        super(RegisterStock, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class UpdateStock(forms.ModelForm):
    class Meta:
        model = models.MonitoredStock
        fields = ['upper_tunnel_bound', 'lower_tunnel_bound', 'periodicity']

    def __init__(self, *args, **kwargs):
        super(UpdateStock, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'