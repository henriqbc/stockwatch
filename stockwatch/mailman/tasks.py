from celery import shared_task
from django.contrib.auth.models import User
from stockwatch.settings import EMAIL_HOST_USER
from ..stocks.models import MonitoredStock, StockUpdate

RECOMMEND_BUYING = 1
RECOMMEND_SELLING = 2

@shared_task
def send_stock_price_alert_email(stock: MonitoredStock, stock_update: StockUpdate):
    if stock_update.price > stock.upper_tunnel_bound:
        recommendation_type = RECOMMEND_BUYING

    elif stock_update.price < stock.lower_tunnel_bound:
        recommendation_type = RECOMMEND_SELLING

    subject = f'Recommended {'selling' if recommendation_type == RECOMMEND_SELLING else 'buying'} of {stock.name} stocks.'

    message = f'''Hi {User.username}!\n\n We have detected a {'drop' if recommendation_type == RECOMMEND_SELLING else 'rise'}
    on the price of {stock.name} shares, which have exceeded the specified monitoring limit. Stockwatch recommends 
    {'selling' if recommendation_type == RECOMMEND_SELLING else 'buying'} such shares.'''

    User.email_user(
        subject = subject,
        message = message,
        from_email = EMAIL_HOST_USER,
        fail_silently = True
    )
