from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Import User model   
from .models import Product,UserAddress, Checkout, Order, Return, Subscriber


class SignUpForm(UserCreationForm):
    # Add any additional fields you want to include in the signup form
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include any additional fields here

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'image']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address', 'payment_method']

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'first_name',
            'last_name',
            'company_name',
            'address',
            'apartment_suite',
            'state_country',
            'postal_zip',
            'email',
            'phone',
        ]

class CheckoutForm(forms.Form):
    selected_shipping_address = forms.ModelChoiceField(
        queryset=UserAddress.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label='Select Shipping Address',
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['selected_shipping_address'].queryset = UserAddress.objects.filter(user=user)
from django import forms
from .models import ReturnItem, Return

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = ReturnItem
        fields = ['product', 'size', 'quantity']

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['return_reason', 'additional_comments']


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

# newsletter/forms.py
from django import forms
from .models import Subscriber

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
