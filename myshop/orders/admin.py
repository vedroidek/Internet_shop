from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """ The model is included inline when displaying
    order information on the admin page. """
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Display order information on the admin page. """
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated', 'stripe_id']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
