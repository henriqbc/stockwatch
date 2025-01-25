from django.urls import path, include
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.stocks_list, name='list'),
    path('<slug:name>', views.stock_page, name='page')
]