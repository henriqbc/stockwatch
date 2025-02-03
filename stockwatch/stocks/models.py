from django.db import models

MAX_STR_FIELD_SIZE = 150

class MonitoredStock(models.Model):
    name = models.CharField(max_length=MAX_STR_FIELD_SIZE, unique=True)
    upper_tunnel_bound = models.FloatField()
    lower_tunnel_bound = models.FloatField()
    periodicity = models.IntegerField()

    def __str__(self):
        return self.name

class StockUpdate(models.Model):
    stock_id = models.ForeignKey('MonitoredStock', on_delete=models.CASCADE, default=1)
    price = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)