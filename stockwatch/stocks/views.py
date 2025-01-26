from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth.decorators import login_required

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
            new_stock.user = request.user
            new_stock.save()
            return redirect('stocks:list')
    else:
        form = forms.RegisterStock()
    return render(request, 'stocks/new_stock.html', {'form':form})