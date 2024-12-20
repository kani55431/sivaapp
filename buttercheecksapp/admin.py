from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, Product, Checkout, Cart, OrderItem, UserAddress, SizeQuantity, Size, Subscriber

admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(Checkout)
admin.site.register(UserAddress)
admin.site.register(Size)
admin.site.register(SizeQuantity)
admin.site.register(Subscriber)
