from django.urls import path
from . import views

app_name = 'subscriber'

urlpatterns = [
    path('home/', views.user_page, name='home'),
    path('subscribe/', views.user_subscribe, name='subscribe'),
]