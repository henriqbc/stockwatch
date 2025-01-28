from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth.decorators import login_required
from stockwatch.settings import REQUEST_PATH_BUILDER
import requests

def stock_home(request):
    if request.user.is_authenticated:
        return redirect('stocks:list')

    return render(request, 'stocks/stock_home.html')

@login_required(login_url="/users/home/")
def stock_page(request, name):
    stock = models.MonitoredStock.objects.get(name = name)
    return render(request, 'stocks/stock_page.html', {'stock':stock})

@login_required(login_url="/users/home/")
def stocks_list(request):
    stocks = models.MonitoredStock.objects.filter(user = request.user)

    if len(stocks) == 0:
        return redirect('stocks:new')
    
    return render(request, 'stocks/stocks_list.html', {'stocks':stocks})

@login_required(login_url="/users/home/")
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

            new_stock.user = request.user
            new_stock.save()
            return redirect('stocks:list')
    else:
        form = forms.RegisterStock()
    return render(request, 'stocks/new_stock.html', {'form':form})