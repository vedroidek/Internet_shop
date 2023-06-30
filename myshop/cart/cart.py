from decimal import Decimal
from django.conf import settings
from Internet_shop.myshop.shop.models import Product


class Cart:
    def __init__(self, request):
        """ Initial cart """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart to session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
