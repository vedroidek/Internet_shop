from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    """ Coupon model.
     Contains data:
     a unique coupon code,
     the beginning and end of the coupon,
     percentage discount,
     whether the coupon is valid.
     """
    code = models.CharField(max_length=64, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)],
                                   help_text='Percentage value (0 to 100)')
    active = models.BooleanField()

    def __str__(self):
        return self.code
