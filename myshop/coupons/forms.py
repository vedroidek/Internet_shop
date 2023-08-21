from django import forms


class CouponApplyForm(forms.Form):
    """ Coupon code form. """
    code = forms.CharField()
