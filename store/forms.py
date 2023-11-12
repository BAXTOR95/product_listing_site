from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product


class PurchaseForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(), empty_label='Select a Product'
    )
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        field = ['username', 'email', 'password1', 'password2']
