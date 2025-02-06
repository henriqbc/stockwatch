from django.shortcuts import render, redirect
from . import models, forms
from stockwatch.settings import REQUEST_PATH_BUILDER
import requests
from subscriber.utils import get_username, AuthenticationError, StockListFetchingError
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from . import tasks

AVAILABLE_STOCKS_PATH = 'https://brapi.dev/api/available'

def stock_home(request):
    try:
        get_username()
    except AuthenticationError:
        return render(request, 'stocks/stock_home.html')
    
    return redirect('stocks:list')

def stock_page(request, name):
    stock = models.MonitoredStock.objects.get(name = name)
    stock_history = models.StockUpdate.objects.filter(stock_id = stock.id).order_by('time')
    return render(request, 'stocks/stock_page.html', {'stock':stock, 'update_history': stock_history})

def stocks_list(request):
    stocks = models.MonitoredStock.objects.all()

    if len(stocks) == 0:
        return redirect('stocks:new')
    
    return render(request, 'stocks/stocks_list.html', {'stocks':stocks})

def new_stock(request):
    try:
        response = requests.get(AVAILABLE_STOCKS_PATH)
        data = response.json().get('stocks', [])
        available_stock = [(stock, stock) for stock in data]
    except requests.exceptions.RequestException:
        raise StockListFetchingError

    if request.method == 'POST':
        form = forms.RegisterStock(request.POST, request.FILES, choices=available_stock)

        print(request.POST)

        if form.is_valid():
            new_stock = form.save(commit=False)
            
            try:
                response = requests.get(REQUEST_PATH_BUILDER(new_stock.name))
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                error_message: str
                match response.status_code:
                    case 400: error_message = 'Request is invalid or improperly formatted.'
                    case 404: error_message = f'Stock {new_stock.name} does not exist.'
                    case _: error_message = ''

                form.add_error(None, f'Error {response.status_code}: "{error_message}".')
                return render(request, 'stocks/new_stock.html', {'form':form})

            try:
                new_stock.save()
            except IntegrityError:
                form.add_error(None, f'Error: Stock with name {new_stock.name} already exists.')

            tasks.schedule_periodic_check.delay(model_to_dict(new_stock))

            return redirect('stocks:list')
        else:
            return render(request, 'stocks/new_stock.html', {'form':form})
                
    else:
        form = forms.RegisterStock()
        form.fields['name'].choices = available_stock

        return render(request, 'stocks/new_stock.html', {'form':form})

def update_stock_config(request, name):
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
    try:
        models.MonitoredStock.objects.filter(name = name).delete()
        tasks.unschedule_periodic_check(stock_name = name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist

    return redirect('stocks:list')

def delete_all_stocks(request):
    tasks.unschedule_all_periodic_checks()
    models.MonitoredStock.objects.all().delete()

    return redirect('stocks:list')
    
def clear_stock_history(request, name):
    try:
        stock = models.MonitoredStock.objects.get(name = name)
    except ObjectDoesNotExist:
        raise AuthenticationError
    
    models.StockUpdate.objects.filter(stock_id = stock.id).delete()

    return redirect('stocks:page', name = name)