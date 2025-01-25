from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.user_home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]