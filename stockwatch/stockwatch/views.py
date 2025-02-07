from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')

def server_error(request):
    return render(request, 'server_error.html')