from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import reverse
from .tasks import order_created
from cart.cart import Cart
from orders.forms import OrderCreateForm
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import OrderItem, Order


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


@staff_member_required
def admin_order_detail(request, order_id):
    """ Order information displayed only for
     users with administrator status. """
    order = get_object_or_404(Order, id-order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})
