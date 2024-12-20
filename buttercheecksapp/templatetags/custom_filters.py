from django import template

register = template.Library()

@register.filter
def calculate_total_price(product_price, quantity):
    return product_price * quantity
from django import template
from django import template
from ..models import SizeQuantity

register = template.Library()

@register.filter(name='available_sizes')
def available_sizes(product):
    return SizeQuantity.objects.filter(product=product, quantity__gt=0).values_list('size__name', flat=True)


from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)
# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='get_available_sizes')
def get_available_sizes(available_sizes, product_id):
    return available_sizes.get(product_id, [])

