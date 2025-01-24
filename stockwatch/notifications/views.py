from django.shortcuts import render

def register_email(request):
    return render(request, 'notifications/notifications.html')
