from django.shortcuts import render, redirect
from . import models, forms
from stockwatch.settings import REQUEST_PATH_BUILDER, AVAILABLE_STOCKS_PATH
import requests
from subscriber.utils import get_username, AuthenticationError, StockListFetchingError
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from . import tasks

def stock_home(request):
    try:
        get_username()
    except AuthenticationError:
        return render(request, 'stocks/stock_home.html')
    except Exception as e:
        return render(request, 'server-error.html')

    return redirect('stocks:list')

def stock_page(request, name):
    try:
        stock = models.MonitoredStock.objects.get(name=name)
        stock_history = models.StockUpdate.objects.filter(stock_id=stock.id).order_by('time')
        return render(request, 'stocks/stock_page.html', {'stock': stock, 'update_history': stock_history})
    except Exception as e:
        return render(request, 'server-error.html')

def stocks_list(request):
    try:
        stocks = models.MonitoredStock.objects.all()

        if len(stocks) == 0:
            return redirect('stocks:new')

        return render(request, 'stocks/stocks_list.html', {'stocks': stocks})
    except Exception as e:
        return render(request, 'server-error.html')

def new_stock(request):
    try:
        response = requests.get(AVAILABLE_STOCKS_PATH)
        data = response.json().get('stocks', [])
        available_stock = [(stock, stock) for stock in data]
    except requests.exceptions.RequestException:
        raise StockListFetchingError
    except Exception as e:
        return render(request, 'server-error.html')

    if request.method == 'POST':
        form = forms.RegisterStock(request.POST, request.FILES, choices=available_stock)

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
                return render(request, 'stocks/new_stock.html', {'form': form})

            try:
                new_stock.save()
            except IntegrityError:
                form.add_error(None, f'Error: Stock with name {new_stock.name} already exists.')

            tasks.schedule_periodic_check(new_stock)
            tasks.stock_price_updater(new_stock.id, new_stock.name, new_stock.upper_tunnel_bound, new_stock.lower_tunnel_bound)

            return redirect('stocks:list')
        else:
            return render(request, 'stocks/new_stock.html', {'form': form})

    else:
        form = forms.RegisterStock()
        form.fields['name'].choices = available_stock

        return render(request, 'stocks/new_stock.html', {'form': form})

def update_stock_config(request, name):
    try:
        stock = models.MonitoredStock.objects.get(name=name)

        if request.method == 'POST':
            form = forms.UpdateStock(request.POST, instance=stock)
            if form.is_valid():
                form.save()
                return redirect('stocks:page', name=name)
        else:
            form = forms.UpdateStock(instance=stock)

        return render(request, 'stocks/update_stock.html', {'form': form, 'name': name})

    except Exception as e:
        return render(request, 'server-error.html')

def delete_stock(request, name):
    try:
        models.MonitoredStock.objects.filter(name=name).delete()
        tasks.unschedule_periodic_check(stock_name=name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist
    except Exception as e:
        return render(request, 'server-error.html')

    return redirect('stocks:list')

def delete_all_stocks(request):
    try:
        tasks.unschedule_all_periodic_checks()
        models.MonitoredStock.objects.all().delete()
    except Exception as e:
        return render(request, 'server-error.html')

    return redirect('stocks:list')

def clear_stock_history(request, name):
    try:
        stock = models.MonitoredStock.objects.get(name=name)
    except ObjectDoesNotExist:
        raise AuthenticationError
    except Exception as e:
        return render(request, 'server-error.html')

    models.StockUpdate.objects.filter(stock_id=stock.id).delete()

    return redirect('stocks:page', name=name)