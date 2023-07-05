from django.shortcuts import render

from Internet_shop.myshop.cart.cart import Cart
from Internet_shop.myshop.orders.forms import OrderCreateForm
from Internet_shop.myshop.orders.models import OrderItem


def order_create(request):
    """ The view receives data from the form to create a new order. """
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'], quantity=item['quantity'])

                cart.clear()
                return render(request, 'orders/order/created.html', {'order': order})
        else:
            form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})