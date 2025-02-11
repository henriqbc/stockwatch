from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('server-error/', views.server_error, name='server-error'),
    path('stocks/', include('stocks.urls')),
    path('user/', include('subscriber.urls')),
]