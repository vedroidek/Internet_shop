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

    def add(self, product: str, quantity: int = 1, override_quantity: bool = False) -> None:
        """ Add a product to the cart or update its quantity. """
        product_id = f'{product.id}'
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': f'{product.price}'}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        #  mark the session as "modified" to ensure it persists
        self.session.modified = True

    def remove(self, product: str) -> None:
        """ Remove item from cart. """
        product_id = f'{product.id}'
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
