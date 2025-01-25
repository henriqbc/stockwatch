from django.shortcuts import render
from django.http import HttpResponse
from . import models

def stocks_list(request):
    stocks = models.MonitoredStock.objects.all().order_by('name')

    if len(stocks) == 0:
        return render(request, 'stocks/stocks_home.html')
    
    return render(request, 'stocks/stocks_list.html', {'stocks':stocks})

def stock_page(request, name):
    stock = models.MonitoredStock.objects.get(name = name)
    return render(request, 'stocks/stock_page.html', {'stock':stock})