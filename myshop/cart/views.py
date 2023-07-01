from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from Internet_shop.myshop.cart.cart import Cart
from Internet_shop.myshop.cart.forms import CartAddProductForm
from Internet_shop.myshop.shop.models import Product


@require_POST
def cart_add(request, product_id):
    """ Adding items to the cart or updating their quantity. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """ Remove product from cart by id. """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    """ Template link function for cart_add and cart_remove. """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})