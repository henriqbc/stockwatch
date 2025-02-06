from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from django.apps import apps
import json
import requests
from stockwatch.settings import REQUEST_PATH_BUILDER
from mailman.handlers import send_stock_price_alert_email
import logging

def unschedule_periodic_check(stock_name):
    try:
        task_name = stock_name.lower() + '_updater'
        periodic_task = PeriodicTask.objects.get(name=task_name)
        periodic_task.delete()
    except PeriodicTask.DoesNotExist:
        logging.warning(f"Periodic task for stock {stock_name} not found.")

def unschedule_all_periodic_checks():
    PeriodicTask.objects.all().delete()

@shared_task
def schedule_periodic_check(stock):

    scheduler = IntervalSchedule.objects.get_or_create(
        every = stock.periodicity,
        period = IntervalSchedule.MINUTES
    )

    args = json.dumps({
        'stock_id': stock.id,
        'stock_name': stock.name,
        'upper_tunnel_bound': stock.upper_tunnel_bound,
        'lower_tunnel_bound': stock.lower_tunnel_bound,
    })

    PeriodicTask.objects.update_or_create(
        name = stock.name.lower() + '_updater',
        defaults={
            "interval": scheduler,
            "task": "stocks.tasks.stock_price_updater",
            "args": args,
        }
    )

@shared_task(store_errors_even_if_ignored=True, ignore_result=True)
def stock_price_updater(stock_id: int, stock_name: str, upper_tunnel_bound: int, lower_tunnel_bound: int):
    try:
        response = requests.get(REQUEST_PATH_BUILDER(stock_name))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Problems with query")
        logging.error(f"Failed to fetch stock price for {stock_name}: {str(e)}")
        return
    
    print("Ran query with api with no problems")

    stock_price = response.json()['regularMarketPrice']

    StockUpdate = apps.get_model(app_label='stocks', model_name='StockUpdate')

    StockUpdate(stock_id = stock_id, price = stock_price).save()

    if stock_price > upper_tunnel_bound:
        send_stock_price_alert_email(stock_name, stock_price, upper_tunnel_bound, True)
    elif stock_price < lower_tunnel_bound:
        send_stock_price_alert_email(stock_name, stock_price, lower_tunnel_bound, False)
