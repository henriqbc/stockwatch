import json
import logging
import requests
from django_q.models import Schedule
from stocks.models import MonitoredStock, StockUpdate
from stockwatch.settings import REQUEST_PATH_BUILDER
from mailman.handlers import send_stock_price_alert_email
from django.core.exceptions import ObjectDoesNotExist

INDEFINITELY = -1

def unschedule_periodic_check(stock_name):
    task_name = f"{stock_name.lower()}_updater"
    deleted_count, _ = Schedule.objects.filter(name=task_name).delete()
    if deleted_count == 0:
        logging.warning(f"Periodic task for stock {stock_name} not found.")

def unschedule_all_periodic_checks():
    Schedule.objects.all().delete()

def schedule_periodic_check(stock):
    task_name = f"{stock.name.lower()}_updater"
    
    args = (stock.id, stock.name, stock.upper_tunnel_bound, stock.lower_tunnel_bound)
    
    Schedule.objects.update_or_create(
        name=task_name,
        defaults={
            "func": "stocks.tasks.stock_price_updater",
            "args": args,
            "schedule_type": Schedule.MINUTES,
            "minutes": stock.periodicity,
            "repeats": INDEFINITELY,  
        }
    )

def stock_price_updater(stock_id, stock_name, upper_tunnel_bound, lower_tunnel_bound):
    try:
        response = requests.get(REQUEST_PATH_BUILDER(stock_name))
        response.raise_for_status()
        data = response.json()
        stock_price = data['results'][0]['regularMarketPrice']

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch stock price for {stock_name}: {str(e)}")
        return
    
    try:  
        stock = MonitoredStock.objects.get(id=stock_id)
    except ObjectDoesNotExist:
        return

    StockUpdate.objects.create(stock_id=stock, price=stock_price)
    
    if stock_price > upper_tunnel_bound:
        send_stock_price_alert_email(stock_name, stock_price, upper_tunnel_bound, True)
    elif stock_price < lower_tunnel_bound:
        send_stock_price_alert_email(stock_name, stock_price, lower_tunnel_bound, False)
