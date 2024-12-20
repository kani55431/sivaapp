# buttercheecks/views.py
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth import logout
from .models import Product, Size, SizeQuantity, Order, Cart, UserAddress
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .templatetags.custom_filters import calculate_total_price  # Import the custom filter
from .forms import OrderForm
from .models import UserAddress
from .forms import UserAddressForm, CheckoutForm
from .models import UserProfile, Order, Cart, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Cart, Checkout, Order, OrderItem
from django.contrib import messages
from .models import Product, SizeQuantity, Cart
from .models import Cart, Checkout, Order, OrderItem
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Cart, Checkout, Order, OrderItem
from django.shortcuts import render, redirect
from .models import UserAddress, Order, OrderItem
from .forms import CheckoutForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, Order, Checkout
from .forms import OrderForm, CheckoutForm
from django.http import JsonResponse
from django.shortcuts import render
from .forms import ProductForm
from django.shortcuts import render
from django.db.models import F

def home(request):
    
    babyswaddles_categories = ['MUSLIN_SWADDLES', 'SNUG_SWADDLES', 'WRAP_SWADDLES', 'BABY_BLANKETS']
    # Retrieve products for the babyswaddles categories
    babyswaddles_products = Product.objects.filter(category__in=babyswaddles_categories, availability=True)
    clothings_catagory=['MUSLIN_ROMBERS', 'MUSLIN_JABLAS']
    clothings_catagory_products=Product.objects.filter(category__in=clothings_catagory, availability=True)
    babybeddings_catagory=['BABY_BEDDINGS']
    babybeddings_catagory_products=Product.objects.filter(category__in=clothings_catagory, availability=True)
    
    
    products = Product.objects.all()  # Retrieve all products from the database
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count()  # Use user.id to filter the Cart objects
    
    context = {'products': products, 'cart_count': cart_count, 'babyswaddles_products':babyswaddles_products, 'clothings_catagory_products':clothings_catagory_products, 'babybeddings_catagory_products':babybeddings_catagory_products} 
    return render(request, 'index.html', context)


def arrivals(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count() 
    products = Product.objects.all()
    context={
        'products':products,
    }
    return render(request, 'products-arrivals.html', context)
from django.contrib.auth import login
from .forms import SignUpForm  # Import your SignUpForm

def signup_login(request):
    products = Product.objects.all()  # Retrieve all products from the database
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        login_form = AuthenticationForm(request, data=request.POST)

        if signup_form.is_valid():
            # Save the user with the email address
            user = signup_form.save(commit=False)
            user.email = signup_form.cleaned_data['email']
            user.save()

            # Log in the user
            login(request, user)
            return redirect('buttercheecksapp:userview')

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('buttercheecksapp:userview')
    else:
        signup_form = SignUpForm()
        login_form = AuthenticationForm()
    
    return render(request, 'login.html', {'signup_form': signup_form, 'login_form': login_form, 'products': products})

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Check if the provided email address exists in the database
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                # If email exists, send the password reset email
                return PasswordResetView.as_view(
                    template_name='password_reset_form.html',
                    success_url=reverse_lazy('password_reset_done')
                )(request)
            else:
                # If email doesn't exist, show a message
                messages.error(request, 'This email is not registered.')
        else:
            messages.error(request, 'Invalid email address.')

    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})


from django.shortcuts import render

def custom_password_reset_done(request):
    return render(request, 'custom_password_reset_done.html')






def user_view(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user).count()
    products = Product.objects.all()  # Retrieve all products from the database
    context = {'products': products, 'cart_count': cart_count,}
    return render(request, 'userlog.html', context)


def logout_view(request):
    logout(request)
    return redirect('buttercheecksapp:signup_login')  # Redirect to your login page



def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('buttercheecksapp:userview')# Redirect to a success page or render a template
    else:
        form = ProductForm()
    return render(request, 'admin/add_product.html', {'form': form})


from django.shortcuts import render

from django.db.models import Q
from django.shortcuts import render
from .models import Product

def product_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(big_description__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()
    
    return render(request, 'product_search_results.html', {'products': products})




def dashboard(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count() 
    products = Product.objects.all()  # Retrieve all products from the database
    context = {'products': products}
    # Fetch data and calculations for the dashboard
    # Pass the necessary context data to the template
    return render(request, 'dashboard.html', context)


def shop(request):  
    products = Product.objects.all()
    available_sizes = {}  
    # Create a dictionary to store available sizes for each product
    for product in products:
        available_sizes[product.id] = SizeQuantity.objects.filter(product=product, quantity__gt=0).values_list('size__name', flat=True)
    return render(request, 'shop.html', {'products': products, 'available_sizes': available_sizes})



def product_detail(request, product_id):
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count() 
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'shop-single.html', context)

def singleshop(request):
    products = Product.objects.all()
    similar_products= Product.objects.all()

    available_sizes = {}
    # Create a dictionary to store available sizes for each product
    for product in products:
        available_sizes[product.id] = SizeQuantity.objects.filter(product=product, quantity__gt=0).values_list('size__name', flat=True)
    return render(request, 'shop-single.html', {'products': products, 'available_sizes':available_sizes, 'similar_products':similar_products})


def address(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count() 
    products = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('checkout', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'address.html', {'form': form, 'products':products})

# views.py

import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
# views.py

import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order

logger = logging.getLogger(__name__)

@csrf_exempt
def update_order_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            order_id = data.get('order_id')
            payment_id = data.get('payment_id')

            try:
                order = Order.objects.get(id=order_id)
                order.status = 'success'
                order.razorpay_payment_id = payment_id
                order.save()

                return JsonResponse({'success': True})
            except Order.DoesNotExist:
                logger.error(f"Order with ID {order_id} not found.")
                return JsonResponse({'error': 'Order not found'}, status=404)
            except Exception as e:
                logger.error(f"Error updating order status: {str(e)}")
                return JsonResponse({'error': 'Failed to update order status'}, status=500)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON data: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def payment(request, order_id):
    user = request.user
    cart_count = Cart.objects.filter(user=user.id).count() 
    order = Order.objects.get(pk=order_id)
    return render(request, 'payment.html', {'order': order})

def success(request, order_id):
    order = Order.objects.get(id=order_id)
    # You can update the order status here if needed
    order.status = 'success'
    order.save()
    return render(request, 'thankyou.html', )

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to add items to your cart.')
        return redirect('buttercheecks:signup_login')

    if request.method == 'POST':
        # Get the selected size and quantity from the form
        size_id = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        
        try:
            # Attempt to convert size_id to an integer
            size_id = int(size_id)
        except ValueError:
            # Handle the case where size_id is not a valid integer
            messages.error(request, 'Invalid size selected.')
            return redirect('buttercheecksapp:product_detail', product_id=product_id)
        
        # Check if the selected size is valid for this product
        size_quantity = SizeQuantity.objects.filter(product=product, size_id=size_id, quantity__gt=0).first()

        if size_quantity:
            # Check if the user already has this product in their cart with the same size
            cart_item = Cart.objects.filter(user=user, product=product, size=size_quantity.size).first()

            if cart_item:
                # Update the quantity if the item is already in the cart
                cart_item.quantity += quantity
                cart_item.save()
            else:
                # Create a new cart item if it doesn't exist
                Cart.objects.create(user=user, product=product, size=size_quantity.size, quantity=quantity)
            
            messages.success(request, 'Product added to your cart successfully.')
            return redirect('buttercheecksapp:cart')
        else:
            messages.error(request, 'The selected size is not available for this product.')

    return redirect('buttercheecksapp:product_detail', product_id=product_id)





@login_required
def cart(request):
    user = request.user
    cart_count = Cart.objects.filter(user=user).count()
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    total_cart_price = 0  # Initialize total cart price

    for cart_item in cart_items:
        total_item_price = cart_item.product.price * cart_item.quantity
        cart_item.total_price = total_item_price
        total_cart_price += total_item_price

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart_price': total_cart_price})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('buttercheecksapp:cart')

from django.db import transaction  # Import the transaction module
from decimal import Decimal
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserAddress, Cart, Checkout, Order, OrderItem, SizeQuantity
from .forms import CheckoutForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import CheckoutForm  # Import your CheckoutForm class
from .models import UserAddress, Cart, Checkout, Order, OrderItem, SizeQuantity
from django.conf import settings
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
import uuid

from django.shortcuts import render, redirect
from django.conf import settings
from django.db import transaction
from .forms import CheckoutForm  # Import your CheckoutForm from forms.py
from .models import UserAddress, Cart, Checkout, Order
import razorpay
from django.shortcuts import render, redirect
from django.db import transaction
from django.conf import settings
from .models import Order, Checkout
from .forms import CheckoutForm  # Make sure to import your CheckoutForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Checkout, Order
from .forms import CheckoutForm  # Make sure to import your CheckoutForm

import razorpay
from django.shortcuts import redirect

from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm  # Make sure to import your CheckoutForm
from .models import UserAddress, Cart, Checkout, Order
import razorpay
from django.conf import settings

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserAddress, Cart, Checkout, Order, OrderItem
from .forms import CheckoutForm
from django.conf import settings
import razorpay

@csrf_exempt
@login_required
def checkout(request):
    user = request.user
    addresses = UserAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    total_cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    total_cart_price_in_paisa = int(total_cart_price * 100)

    if request.method == 'POST':
        form = CheckoutForm(user, request.POST)
        if form.is_valid():
            selected_address = form.cleaned_data['selected_shipping_address']
            razorpay_payment_id = request.POST.get('razorpay_payment_id')

            # Create or update the checkout instance with the selected address
            try:
                checkout = Checkout.objects.get(user=user)
                checkout.shipping_address = selected_address
                checkout.save()
            except Checkout.DoesNotExist:
                checkout = Checkout.objects.create(user=user, shipping_address=selected_address)

            # Create the order and associate it with the checkout
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    shipping_address=str(checkout.shipping_address.shipping_address),
                    billing_address=str(checkout.shipping_address.shipping_address),
                    payment_method='Online Payment',
                    total_amount=total_cart_price,
                    status='pending',
                )

                # Save product details in the order
                for cart_item in cart_items:
                    order_item = OrderItem.objects.create(
                        user=user,
                        product=cart_item.product,
                        order=order,
                        quantity=cart_item.quantity,
                        item_price=cart_item.product.price,
                    )

                # Initialize Razorpay client with your API key and secret
                razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

                # Create a Razorpay order
                razorpay_order = razorpay_client.order.create({
                    'amount': total_cart_price_in_paisa,  # Convert to paisa
                    'currency': 'INR',
                    'payment_capture': 1,  # Auto-capture payment when the order is placed
                })

                # Save Razorpay order details to the order
                order.razorpay_order_id = razorpay_order['id']
                order.razorpay_payment_id = razorpay_payment_id
                order.save()

                # Clear the cart after successful checkout
                cart_items.delete()

                messages.success(request, 'Order placed successfully!')
                return redirect('buttercheecksapp:success')
        else:
            # Handle form validation errors
            return JsonResponse({'error': 'Invalid form data.'}, status=400)
    else:
        form = CheckoutForm(user)

    context = {
        'addresses': addresses,
        'form': form,
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'total_cart_price_in_paisa': total_cart_price_in_paisa,
        'user': user,
    }

    return render(request, 'checkout.html', context)



from django.http import JsonResponse
from .models import Order

def update_order_payment_id(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')

        try:
            order = Order.objects.get(id=order_id)
            order.razorpay_payment_id = payment_id
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))


# views.py

from django.http import HttpResponse, HttpResponseBadRequest
import json



from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt









@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'payment.html', {'order': order})
# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .models import Cart
from django.shortcuts import render, redirect
from django.contrib import messages

@login_required
def success(request):
    try:
        # Retrieve the latest order for the logged-in user
        order = Order.objects.filter(user=request.user).latest('created_at')
        
        # Update the order status to 'placed'
        order.status = 'placed'
        order.save()

        # Clear the user's cart items
        Cart.objects.filter(user=request.user).delete()

        context = {'order': order}
        return render(request, 'thankyou.html', context)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('buttercheecksapp:checkout')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('buttercheecksapp:checkout')



@login_required
def order_details(request, order_id):
    # Ensure that the order with the given ID belongs to the current user
    user = request.user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order_id=order_id)
    checkout = Checkout.objects.filter(user=user, order=order).first()
    
    
    for order_item in order_items:
        order_item.total_amount = order_item.quantity * order_item.item_price
    
    # Prepare a dictionary with the order data
    order_details = {
        'order': order,
        'order_items': order_items,
        'checkout':checkout,
        
    }

    # Render the order details template with the order data
    return render(request, 'order_details.html', order_details)


@login_required
def order_history(request):
    # Retrieve the user's orders
    
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders,
    }

    return render(request, 'order_history.html', context)



@login_required
def user_profile(request):
    # Retrieve the user object
    user = request.user
    addresses = UserAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    total_cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    total_cart_price = 0  # Initialize total cart price

    for cart_item in cart_items:
        total_item_price = cart_item.product.price * cart_item.quantity
        cart_item.total_price = total_item_price
        total_cart_price += total_item_price

    # Attempt to retrieve the user's profile, or create one if it doesn't exist
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Create a new UserProfile if it doesn't exist
        profile = UserProfile.objects.create(user=user)
    
    # Retrieve the user's cart
    cart_items = Cart.objects.filter(user=user)
    
    # Retrieve the user's checkout details
    try:
        checkout = Checkout.objects.get(user=user)
    except Checkout.DoesNotExist:
        # Create a new Checkout if it doesn't exist
        checkout = Checkout.objects.create(user=user)
    
    # Retrieve the user's orders
    orders = Order.objects.filter(user=user)
    
    # Retrieve the order items for each order
    order_items = OrderItem.objects.filter(user=user)
    
    # Prepare the data to be returned
    user_details = {
        'username': user.username,
        'email': user.email,
        'profile': profile,
        'cart_items': cart_items,
        'checkout': checkout,
        'orders': orders,
        'order_items': order_items,
        'total_cart_price':total_cart_price,
        'addresses':addresses,
    }
    
    return render(request, 'user_profile.html', user_details)



@login_required
def orders(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    total_cart_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    total_cart_price = 0  # Initialize total cart price

    for cart_item in cart_items:
        total_item_price = cart_item.product.price * cart_item.quantity
        cart_item.total_price = total_item_price
        total_cart_price += total_item_price

    # Attempt to retrieve the user's profile, or create one if it doesn't exist
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        # Create a new UserProfile if it doesn't exist
        profile = UserProfile.objects.create(user=user)
    
    # Retrieve the user's cart
    cart_items = Cart.objects.filter(user=user)
    
    # Retrieve the user's checkout details
    try:
        checkout = Checkout.objects.get(user=user)
    except Checkout.DoesNotExist:
        # Create a new Checkout if it doesn't exist
        checkout = Checkout.objects.create(user=user)
    
    # Retrieve the user's orders
    orders = Order.objects.filter(user=user)
    
    # Retrieve the order items for each order
    order_items = OrderItem.objects.filter(user=user)
    
    # Prepare the data to be returned
    user_details = {
        'username': user.username,
        'email': user.email,
        'profile': profile,
        'cart_items': cart_items,
        'checkout': checkout,
        'orders': orders,
        'order_items': order_items,
        'total_cart_price':total_cart_price,
    }
    
    return render(request, 'orders.html', user_details)



def manage_addresses(request):
    user = request.user
    addresses = UserAddress.objects.filter(user=user)
    context = {'addresses': addresses}
    
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            return redirect('buttercheecksapp:checkout')
    else:
        form = UserAddressForm()

    context['form'] = form
    return render(request, 'manage_addresses.html', context)


def address(request):
    user = request.user
    addresses = UserAddress.objects.filter(user=user)
    context = {'addresses': addresses}
    return render(request, 'address.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserAddress
from .forms import UserAddressForm

def edit_address(request, address_id):
    user = request.user
    address = get_object_or_404(UserAddress, id=address_id, user=user)

    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('buttercheecksapp:address')  # Redirect to the address list page
    else:
        form = UserAddressForm(instance=address)

    context = {'form': form, 'address': address}
    return render(request, 'edit_address.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import UserAddress
from django.contrib.auth.decorators import login_required

@login_required
def delete_address(request, address_id):
    user = request.user
    address = get_object_or_404(UserAddress, id=address_id, user=user)

    if request.method == 'POST':
        address.delete()
    
    return redirect('buttercheecksapp:address')  # Redirect to the address list page

from django.db import transaction

from django.shortcuts import get_object_or_404, redirect, render
from .models import Order

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        cancellation_reason = request.POST.get('cancellation_reason')
        if cancellation_reason:
            order.status = 'canceled'
            order.cancellation_reason = cancellation_reason
            order.save()
            # Optionally, you can send a confirmation email to the user here.

        return redirect('buttercheecksapp:orders')

    return render(request, 'cancel_order.html', {'order': order})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Return
from .forms import ReturnForm
from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, Return
from .forms import ReturnForm  # Import your ReturnForm

from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Return, ReturnItem
from .forms import ReturnForm, ReturnItemForm  # Import your ReturnItemForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Return, ReturnItem
from .forms import ReturnForm

def request_return(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        return_form = ReturnForm(request.POST)
        if return_form.is_valid():
            # Create the return request
            return_request = return_form.save(commit=False)
            return_request.order = order
            return_request.user = request.user  # Assuming you're using authentication
            return_request.save()

            # Create return items based on order details
            for order_item in order.orderitem_set.all():
                product = order_item.product
                quantity = order_item.quantity

                # Create a ReturnItem without a size attribute
                return_item = ReturnItem(
                    return_request=return_request,
                    product=product,
                    quantity=quantity
                )
                return_item.save()

            return redirect('buttercheecksapp:return_request_confirmation')

    else:
        # Create an empty ReturnForm
        return_form = ReturnForm()

    context = {
        'return_form': return_form,
        'order': order,
    }

    return render(request, 'request_return.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def create_review(request, order_id):
    product = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('buttercheecksapp:review_submitted')
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form, 'product': product})

def review_submitted(request):
    return render(request, 'review_submitted.html')


def return_request_confirmation(request):
    return render(request, 'return_request_confirmation.html')

from django.shortcuts import render, get_object_or_404
from .models import Return

def return_details(request, return_id):
    return_obj = get_object_or_404(Return, id=return_id)

    context = {
        'return': return_obj,
    }

    return render(request, 'return_details.html', context)


from django.shortcuts import render
from .models import Product

def product_list_by_category(request, category):
    products = Product.objects.filter(category=category, availability=True)
    context = {'products': products, 'category_name': category, }
    return render(request, 'products.html', context)


def about(request):
    return render(request, 'about.html')




def generate_invoice(request, order_id):
    # Fetch the order details and order items from your model
    order = Order.objects.get(pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    context = {'order_items': order_items, 'order':order}

    return render(request, 'order_invoice.html', context)


#4.12.2023

def swaddles_blankets(request):

    babyswaddles_categories = ['MUSLIN_SWADDLES', 'SNUG_SWADDLES', 'WRAP_SWADDLES', 'BABY_BLANKETS']
    # Retrieve products for the babyswaddles categories
    babyswaddles_products = Product.objects.filter(category__in=babyswaddles_categories, availability=True)
    
    
    context={  'babyswaddles_products':babyswaddles_products,

    }
    return render(request, 'catagory/swaddles_blankets.html', context)



def clothings(request):
    clothings_catagory=['MUSLIN_ROMBERS', 'MUSLIN_JABLAS']
    clothings_catagory_products=Product.objects.filter(category__in=clothings_catagory, availability=True)
    context={
'clothings_catagory_products':clothings_catagory_products
    }
    return render(request, 'catagory/clothings.html', context)


def nursing_supplies(request):
    nursing_supplies_catagory=['BURP_CLOTH SETS', 'BIB_CLOTH SETS']
    
    nursing_supplies_catagory_products=Product.objects.filter(category__in=nursing_supplies_catagory, availability=True)
    
    context={
'nursing_supplies_catagory_products':nursing_supplies_catagory_products
    }
    return render(request, 'catagory/Nursing_supplies.html', context)


def baby_beddings(request):
    babybeddings_catagory=['BABY_BEDDINGS']
    babybeddings_catagory_products=Product.objects.filter(category__in=babybeddings_catagory, availability=True)
    
    context={
'babybeddings_catagory_products':babybeddings_catagory_products
    }
    return render(request, 'catagory/baby_beddings.html', context)

def returnrefund(request):
    return render(request, 'catagory/returnandrefund.html')
