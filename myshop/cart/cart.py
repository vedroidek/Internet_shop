from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart:
    """ The session state management class for the user.
    Saves data about the products and their total prices
    added to the cart before the purchase/cancellation/closing of the browser. """

    def __init__(self, request):
        """ Initial cart """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart to session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # save current active coupon
        self.coupon_id = self.session.get('coupon_id')

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

    def __iter__(self) -> Decimal:
        """ Getting the items in the cart from the database. """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[f'{product.id}']['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:  # Mister Obvious :)
        """ Counting all items in the shopping cart. """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self) -> Decimal:
        """ Calculate the sum of all items in the cart in the current session. """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ Remove the cart from session. """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    @property
    def coupon(self):
        """ Looks up a coupon in the database.
        If successful, returns the coupon id. """
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesotExist:
                pass
            return None

    def get_discount(self):
        """ Returns the amount that will be deducted
        from the total amount of the cart.
        Else discount = 0. """
        if self.coupon:
            return (self.coupon.discount / Decimal(100) * self.get_total_price())
        return Decimal(0)

    def get_total_price_after_discount(self):
        """ Will return the final amount of
        the order after deducting the discount. """
        return self.get_total_price() - self.get_discount()
