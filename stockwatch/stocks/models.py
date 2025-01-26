from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse

MAX_STR_FIELD_SIZE = 150

class MonitoredStock(models.Model):
    name = models.CharField(max_length=MAX_STR_FIELD_SIZE)
    upper_tunnel_bound = models.IntegerField()
    lower_tunnel_bound = models.IntegerField()
    periodicity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name

class StockUpdate(models.Model):
    stock_id = models.ForeignKey('MonitoredStock', on_delete=models.CASCADE, default=1)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)