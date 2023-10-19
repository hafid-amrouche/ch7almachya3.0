from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["price","name", "given_price"]
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["price"].widget.attrs["class"] = "form-control"
        self.fields["given_price"].widget.attrs["class"] = "form-control"
        self.fields["name"].widget.attrs["class"] = "form-control"
