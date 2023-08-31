from django import forms
from .models import *


class ItemForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'color', 'jewelry_type', 'material', 'description', 'price', 'quantity', 'image']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['country', 'city_postal', 'shipping_address', 'phone_number', 'pay_with_card']
        labels = {
            'country': 'Country',
            'city_postal': 'City / Postal',
            'shipping_address': 'Shipping Address',
            'phone_number': 'Phone Number',
            'pay_with_card': 'Pay with Card',
        }
        widgets = {
            'pay_with_card': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
