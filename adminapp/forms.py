from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from buttercheecksapp.models import Order, Product, OrderItem, Size, SizeQuantity
class AdminSignupForm(UserCreationForm):
    # Add any additional fields you need
    pass
# forms.py



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['sizes_and_quantities']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Change the label for the price2 field
        self.fields['price2'].label = 'Orginal Price'


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']
# adminapp/forms.py

class SizeQuantityForm(forms.ModelForm):
    class Meta:
        model = SizeQuantity
        fields = '__all__'

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'estimated_delivery_time', 'shipping_by', 'tracking_number']

    # Add widgets for specific fields
    widgets = {
        'estimated_delivery_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }