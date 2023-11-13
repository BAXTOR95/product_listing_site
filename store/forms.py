from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Product, PurchaseProduct


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseProduct
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].empty_label = 'Select a Product'
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].initial = 1
        self.fields['quantity'].min_value = 1

    def clean_quantity(self):
        """
        Custom validation for the 'quantity' field.
        Ensures that the quantity is at least 1.
        """
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise ValidationError("Quantity must be at least 1.")
        return quantity


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
