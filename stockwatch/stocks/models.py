from django.db import models

MAX_STR_FIELD_SIZE = 150

class MonitoredStock(models.Model):
    name = models.CharField(max_length=MAX_STR_FIELD_SIZE, default='BR1')
    upper_tunnel_bound = models.IntegerField()
    lower_tunnel_bound = models.IntegerField()
    periodicity = models.IntegerField()

    def __str__(self):
        return self.name

class StockUpdate(models.Model):
    stock_id = models.ForeignKey("MonitoredStock", on_delete=models.CASCADE)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)