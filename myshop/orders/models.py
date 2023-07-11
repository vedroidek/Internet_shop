from django.db import models
from django.conf import settings
from shop.models import Product


class Order(models.Model):
    """ Detailed information about the order. """
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    address = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=32)
    city = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self) -> str:
        """ Return order id. """
        return f'Order {self.id}'

    def get_total_cost(self) -> int | float:
        """ Total Order Value. Refers to the OrderItem get_cost() method of the model,
        which calculates the cost of a similar item. For each type,
        a subset is made and the total cost of the order is
        determined by enumeration of each position in the list."""
        return sum(item.get_cost() for item in self.items.all())

    def get_stripe_url(self):
        """ Get a full url for a test or real payment. """
        if not self.stripe_id:
        #  no associated payments
            return ''

        if '_test_' in settings.STRIPE_SECRET_KEY:
        #  path for test payments
            path = '/test/'
        else:
        #  path for real payments
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'


class OrderItem(models.Model):
    """ The model stores data about purchased goods. """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.id}'

    def get_cost(self) -> float:
        """ Calculation of the cost of the same type of goods
        by multiplying the quantity by the cost. """
        return self.price * self.quantity
