from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.stocks_list)
]