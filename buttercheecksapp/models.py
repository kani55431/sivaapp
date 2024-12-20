# buttercheecks/models.py
from django.db import models
from django.contrib.auth.models import User
#6.12.2023
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

def validate_image_size(value):
    max_size = settings.MAX_UPLOAD_SIZE
    if value.size > max_size:
        raise ValidationError(_('File size must be no more than %(max_size)s. Current size is %(current_size)s.') % {
            'max_size': filesizeformat(max_size),
            'current_size': filesizeformat(value.size)
        })


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add your additional fields here
    def __str__(self):
        return self.user.username

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
CATEGORY_CHOICES = (
    ('BABY_SWADDLES', 'Baby Swaddles'),
    ('BABY_ROMBERS', 'Baby Rombers'),
    ('BABY_JABLAS', 'Baby Jablas'),
    ('BABY_BLANKETS', 'Baby Blankets'),
    ('BABY_BEDDINGS', 'Baby Beddings'),

    #newly added 9.11.2023
    ('MUSLIN_SWADDLES','Muslin Swaddles'),
('SNUG_SWADDLES', 'Snug Swaddles'),
('WRAP_SWADDLES', 'Wrap Swaddles'),
('MUSLIN_ROMBERS',	'Muslin Rombers'),
('MUSLIN_JABLAS',	'Muslin Jablas'),
('BURP_CLOTH SETS','Burp Cloth Sets'),
('BIB_CLOTH SETS','Bib Cloth Sets'),
('BABY_BED_SETS', 'Baby Bed Sets')


    
)
class Product(models.Model):
   
    product_name = models.CharField(max_length=100)
    color = models.CharField(max_length=15, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price2= models.DecimalField(max_digits=10, decimal_places=2, null=True)
    big_description = models.TextField(null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True)
    availability = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='products/', null=True, validators=[validate_image_size])
    image2 = models.ImageField(upload_to='products/', null=True, validators=[validate_image_size])
    image3 = models.ImageField(upload_to='products/', null=True, validators=[validate_image_size])
    image4 = models.ImageField(upload_to='products/', null=True, validators=[validate_image_size])
    image5 = models.ImageField(upload_to='products/', null=True, validators=[validate_image_size])
    sizes_and_quantities = models.ManyToManyField(Size, through='SizeQuantity')
    description = models.TextField()
    image = models.ImageField(upload_to='products/', validators=[validate_image_size])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    material = models.CharField(max_length=200, null=True)
    age_group = models.CharField(max_length=200, null=True)
    features = models.TextField(null=True)

    def __str__(self):
        return self.product_name
def validate_image_size(value):
    max_size = settings.MAX_UPLOAD_SIZE
    if value.size > max_size:
        raise ValidationError(_('File size must be no more than %(max_size)s. Current size is %(current_size)s.') % {
            'max_size': filesizeformat(max_size),
            'current_size': filesizeformat(value.size)
        })


    
class SizeQuantity(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.product} - {self.size.name}: {self.quantity} available"



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size,  on_delete=models.CASCADE,null=True)  # Add this line
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # Add this field

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.product_name}"
    
    def add_product_to_cart(self, product, quantity=1):
        cart_item, created = Cart.objects.get_or_create(user=self.user, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=255,  null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=100, blank=True)
    state_country = models.CharField(max_length=100)
    postal_zip = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.address}{self.apartment_suite}{self.state_country}{self.postal_zip} {self.phone}"



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.CharField(UserAddress, max_length=255,  null=True)
    billing_address = models.CharField(UserAddress, max_length=255,  null=True)
    payment_method = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    order_id = models.CharField(max_length=8, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery_time = models.DateTimeField(null=True)
    shipping_by = models.CharField(max_length=100, null=True)
    tracking_number = models.CharField(max_length=50, null=True)
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_unique_order_id()
        super().save(*args, **kwargs)

import random

def generate_unique_order_id():
    while True:
        order_id = ''.join(random.choices('0123456789', k=8))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id
 


class Checkout(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    selected_shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, null=True)
    shipping_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='checkout_shipping_address', null=True)

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add a total_amount field to store the calculated total
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate the total amount before saving
        self.total_amount = self.quantity * self.item_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product} (Order #{self.order.id})"



from django.db import models
from .models import Order  # Import your Order model

# models.py

from django.db import models
from django.contrib.auth.models import User  # If you want to associate returns with users
from django.db import models

class Return(models.Model):
    RETURN_REASON_CHOICES = [
        ('damaged', 'Damaged Product'),
        ('wrong_item', 'Received Wrong Item'),
        ('size_issue', 'Size Issue'),
        ('other', 'Other'),
    ]

    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Link the return to a specific order
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # If you want to associate returns with users
    return_reason = models.CharField(max_length=20, choices=RETURN_REASON_CHOICES)
    additional_comments = models.TextField(blank=True)  # Optional additional comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Return for Order #{self.order.id}'

class ReturnItem(models.Model):
    return_request = models.ForeignKey(Return, on_delete=models.CASCADE, related_name='return_items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Replace 'Product' with your actual product model
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Return Item for Return #{self.return_request.id}'


class Review(models.Model):
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
    




#2.12.2023
    
    # newsletter/models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

