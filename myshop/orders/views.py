from django.shortcuts import render, redirect
from django.shortcuts import reverse
from .tasks import order_created
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem


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
                order_created.delay(order.id)
                # create order in session
                request.session['order_id'] = order.id
                # redirect to payment
                return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
