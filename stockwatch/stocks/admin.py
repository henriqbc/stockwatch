from django.contrib import admin

from . import models

admin.site.register(models.MonitoredStock)
admin.site.register(models.StockUpdate)