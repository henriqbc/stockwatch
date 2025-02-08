from django.urls import path, include
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.stock_home, name='home'),
    path('list/', views.stocks_list, name='list'),
    path('new/', views.new_stock, name='new'),
    path('<slug:name>/', views.stock_page, name='page'),
    path('update/<slug:name>/', views.update_stock_config, name='update'),
    path('delete/', views.delete_all_stocks, name='full-delete'),
    path('delete/<slug:name>', views.delete_stock, name='delete'),
]