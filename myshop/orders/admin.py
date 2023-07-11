import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """ The model is included inline when displaying
    order information on the admin page. """
    model = OrderItem
    raw_id_fields = ['product']


def order_stripe_payment(obj):
    """ Displays in the admin panel
    the stripe_id of the order for
    quick navigation to payment details
    on the Stripe platform. """
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_stripe_payment.short_description = 'Stripe payment'


def export_to_csv(modeladmin, request, queryset):
    """ Export orders to a CSV file. """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    #  write header to csv file
    writer.writerow([field.verbose_name for field in fields])
    #  write data string
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Display order information on the admin page. """
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', order_stripe_payment,
                    'created', 'updated', 'stripe_id']

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
