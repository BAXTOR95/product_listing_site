from django import forms
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
