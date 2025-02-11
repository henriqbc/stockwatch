from stockwatch.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from subscriber.utils import get_user_info, AuthenticationError

def send_stock_price_alert_email(
    stock_name: str, 
    stock_price: int, 
    tunnel_bound_crossed: int, 
    recommend_buying: bool):

    try:
        username, user_email = get_user_info()
    except AuthenticationError:
        raise AuthenticationError

    subject = f'Recommended {'buying' if recommend_buying else 'selling'} of {stock_name} stocks.'

    message = f'''Hi {username}!\n\nWe have detected a {'rise' if recommend_buying else 'drop'} on the price of {stock_name} shares, which have exceeded the specified monitoring limit. Stockwatch recommends {'buying' if recommend_buying else 'selling'} such shares.\n\nCurrent Price: {stock_price}\n\n{'Upper' if recommend_buying else 'Lower'} Tunnel Bound (As Configured): {tunnel_bound_crossed}'''

    send_mail(
        subject = subject,
        message = message,
        from_email = EMAIL_HOST_USER,
        recipient_list = [user_email],
        fail_silently = True,
    )
