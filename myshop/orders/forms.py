from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    """ Form for creating objects of 'Orders' """
    class Meta:
        model = Order
        fields = ['first_name', 'lats_name', 'email', 'address', 'postal_code', 'city']
