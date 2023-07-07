from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """ Creating a task to send notifications to the user
    by e-mail upon successful creation of an order. """
    order = Order.objects.get(id=order_id)
    subject = f'Order no.: {order.id}'
    message = f'Dear {order.first_name}, \n\nYou have successfully placed an order.' \
              f'You order ID is {order.id}'
    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
