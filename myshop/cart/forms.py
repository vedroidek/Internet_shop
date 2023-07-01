from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, f'{i}') for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    """ Form for added products in cart. """
    quantity = forms.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
