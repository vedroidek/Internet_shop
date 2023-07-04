from django.db import models


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

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self) -> str:
        """ Return order id. """
        return f'Order {self.id}'

    def get_total_cost(self) -> int | float:
        """ Total Order Value. """
        return sum(item.get_cost() for item in self.items.all())
