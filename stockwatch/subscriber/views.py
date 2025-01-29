from django.shortcuts import render, redirect
from . import models
from . import forms
from django.core.exceptions import ObjectDoesNotExist

def user_page(request):
    return render(request, 'subscriber/home.html')
    
def user_subscribe(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            models.UserModel.objects.update_or_create(
                id = 1,
                defaults = form.cleaned_data
            )

            return redirect('subscriber:home')

    form = forms.UserForm()
    return render(request, 'subscriber/subscribe.html', {'form': form})

def user_reset(request):
    try:
        models.UserModel.objects.get(id=1).delete()
    except ObjectDoesNotExist:
        pass
    
    return redirect('subscriber:home')

