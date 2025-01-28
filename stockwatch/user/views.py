from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from . import forms
from django.contrib.auth import login, logout

def user_home(request):
    return render(request, 'user/user_home.html')

def register_user(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('user:home')

    else:
        form = forms.RegistrationForm()

    return render(request, 'user/register_user.html', {'form':form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('stocks:list')
    else:
        form = AuthenticationForm()
        
    return render(request, 'user/login.html', {'form':form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('user:home')