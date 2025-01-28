from django.shortcuts import render, redirect
from . import models, forms
from stockwatch.settings import REQUEST_PATH_BUILDER
import requests
from stockwatch.context import global_username, NOT_SUSCRIBED
from django.core.exceptions import ObjectDoesNotExist

def stock_home(request):
    if global_username() != NOT_SUSCRIBED:
        return redirect('stocks:list')

    return render(request, 'stocks/stock_home.html')

def stock_page(request, name):
    stock = models.MonitoredStock.objects.get(name = name)
    stock_history = models.StockUpdate.objects.filter(stock_id = stock.id)
    return render(request, 'stocks/stock_page.html', {'stock':stock, 'update_history': stock_history})

def stocks_list(request):
    stocks = models.MonitoredStock.objects.all()

    if len(stocks) == 0:
        return redirect('stocks:new')
    
    return render(request, 'stocks/stocks_list.html', {'stocks':stocks})

def new_stock(request):
    if request.method == 'POST':
        form = forms.RegisterStock(request.POST, request.FILES)
        if form.is_valid():
            new_stock = form.save(commit=False)

            try:
                response = requests.get(REQUEST_PATH_BUILDER(new_stock.name))
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                form.add_error(None, f'Error {response.status_code}: "{response.json()['message']}"')
                return render(request, 'stocks/new_stock.html', {'form':form})

            new_stock.save()
            return redirect('stocks:list')
    else:
        form = forms.RegisterStock()
    return render(request, 'stocks/new_stock.html', {'form':form})

def update_stock(request, name):
    stock = models.MonitoredStock.objects.get(name = name)

    if request.method == 'POST':
        form = forms.UpdateStock(request.POST, instance = stock)
        if form.is_valid():
            form.save()
            return redirect('stocks:page', name = name)
    else:
        form = forms.UpdateStock(instance = stock)
    
    return render(request, 'stocks/update_stock.html', {'form':form, 'name':name})

def delete_stock(request, name):
    models.MonitoredStock.objects.filter(name = name).delete()

    return redirect('stocks:list')

def delete_all_stocks(request):
    models.MonitoredStock.objects.all().delete()

    return redirect('stocks:list')