from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .forms import AdminSignupForm
from buttercheecksapp.models import Product 
from django.contrib.auth.models import User
from django.contrib.auth import logout
from buttercheecksapp.models import Order, Product, OrderItem, SizeQuantity,  Size, Return,  UserAddress , Review

from django.shortcuts import render, get_object_or_404
from .forms import SizeForm,  SizeQuantityForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from django.shortcuts import render, redirect
# ... existing views ...
def admin_login_view(request):
    return LoginView.as_view(template_name='admin_login.html')(request)

def admin_signup_view(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:admin_login')
    else:
        form = AdminSignupForm()
    return render(request, 'admin_signup.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def dashboard_view(request):
    users = User.objects.all()
    username = request.user.username
     # Calculate orders count and total sales
    orders_count = Order.objects.count()
    products_count=Product.objects.count()
    total_sales = sum(order.total_amount for order in Order.objects.all())
    pending_orders_count = Order.objects.filter(status='pending').count()
    delivered_orders_count = Order.objects.filter(status='delivered').count()
    shipping_orders_count = Order.objects.filter(status='shipped').count()
    pending_orders = Order.objects.filter(status='pending').order_by('-created_at')
    top_products = Product.objects.all()[:5]
    order_details = []
    count=orders_count+products_count

    for order in pending_orders:
        order_items = OrderItem.objects.filter(order=order)
        total_amount = sum(item.total_amount for item in order_items)
        order_details.append({
            'order': order,
            'order_items': order_items,
            'total_amount': total_amount,
        })

    context = {
        'orders_count': orders_count,
        'total_sales': total_sales,
        'users': users, 'username': username, 
         'pending_orders_count': pending_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'shipping_orders_count': shipping_orders_count,
        'order_details': order_details,
        'products_count':products_count,
        'top_products': top_products,
        'count':count,
    }
    
    return render(request, 'dashboard.html', context)

def products_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)

def products_images(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products_images.html', context)




def logout_view(request):
    logout(request)
    return redirect('adminapp:admin_login')

from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):
    # Initialize empty querysets for search results
    orders = Product.objects.none()
    products = Product.objects.none()
    users = User.objects.none()

    # Handle search query
    search_query = request.GET.get('q')
    if search_query:
        # Perform search on orders, products, and users
        orders = Order.objects.filter(
            Q(order_id__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
        products = Product.objects.filter(
            Q(product_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        users = User.objects.filter(username__icontains=search_query)
    
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    total_sales = sum(order.total_amount for order in Order.objects.all())
    pending_orders_count = Order.objects.filter(status='pending').count()
    delivered_orders_count = Order.objects.filter(status='delivered').count()
    shipping_orders_count = Order.objects.filter(status='shipped').count()
    pending_orders = Order.objects.filter(status='pending').order_by('-created_at')
    top_products = Product.objects.all()[:5]
    order_details = []

    for order in pending_orders:
        order_items = OrderItem.objects.filter(order=order)
        total_amount = sum(item.total_amount for item in order_items)
        order_details.append({
            'order': order,
            'order_items': order_items,
            'total_amount': total_amount,
        })

    context ={
        'orders_count': orders_count,
        'total_sales': total_sales,
        'users': User.objects.all(),
        'username': request.user.username,
        'pending_orders_count': pending_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'shipping_orders_count': shipping_orders_count,
        'order_details': order_details,
        'products_count': products_count,
        'top_products': top_products,
        'products': products,
        'count': products_count + orders_count,  # This may need adjustment based on your requirements
        'search_results': {
            'orders': orders,
            'products': products,
            'users': users,
        },
    }

    return render(request, 'littlebubsdashboard.html', context)








def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'orderdetails.html', context)


from django.shortcuts import render, redirect
from .forms import ProductForm  # Import your ProductForm from the correct location

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('adminapp:product_list')  # Redirect to the product list view
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'add_product.html', context)


def edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('adminapp:product_list')  # Redirect to the product list view
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    orders = Order.objects.all()
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('adminapp:product_list')  # Redirect to the product list view
    
    return render(request, 'delete_product.html', {'product': product, 'orders':orders})


def product_list(request):
    search_query = request.GET.get('search', '')
    orders = Order.objects.all()

    # Filter products based on the search query
    products = Product.objects.filter(product_name__icontains=search_query)

    # Order the products by creation date in descending order (newest first)
    products = products.order_by('-created_at')

    return render(request, 'product_list.html', {'products': products, 'search_query': search_query, 'orders':orders})


from django.shortcuts import render
from django.shortcuts import render

def order_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the URL parameter
    status_filter = request.GET.get('status', '')  # Get the status filter from the URL parameter

    orders = Order.objects.all()

    # Apply status filter if provided
    if status_filter:
        if status_filter == 'all':
            # Show all orders, no status filter
            pass
        else:
            # Filter orders by selected status
            orders = orders.filter(status=status_filter)

    if search_query:
        # If a search query is provided, filter orders by order_id
        orders = orders.filter(order_id__icontains=search_query)

    return render(request, 'total_orders.html', {
        'orders': orders,
        'search_query': search_query,
        'status_filter': status_filter,  # Pass the status filter to the template
    })




# adminapp/views.py
# sizes craetaion 
def size_list(request):
    sizes=Size.objects.all()
    return render(request, 'sizelist.html', {'sizes':sizes})

def add_size(request):
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:size_list')
    else:
        form = SizeForm()
    
    context = {'form': form}
    return render(request, 'add_size.html', context)

def delete_size(request, size_id):
    size = Size.objects.get(pk=size_id)
    if request.method == 'POST':
        size.delete()
        return redirect('adminapp:size_list')
    
    context = {'size': size}
    return render(request, 'delete_size.html', context)
# adminapp/views.py
# sizequnatity add to products 

def add_size_quantity(request):
    if request.method == 'POST':
        form = SizeQuantityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminapp:size_quantity_management')
    else:
        form = SizeQuantityForm()
    
    context = {'form': form}
    return render(request, 'add_size_quantity.html', context)



def edit_size_quantity(request, size_quantity_id):
    size_quantity = get_object_or_404(SizeQuantity, id=size_quantity_id)

    if request.method == 'POST':
        form = SizeQuantityForm(request.POST, instance=size_quantity)
        if form.is_valid():
            form.save()
            return redirect('adminapp:size_quantity_management') # Redirect to the size quantity detail page
    else:
        form = SizeQuantityForm(instance=size_quantity)

    return render(request, 'edit_size_quantity.html', {'form': form, 'size_quantity': size_quantity})


def delete_size_quantity(request, size_quantity_id):
    size_quantity = SizeQuantity.objects.get(pk=size_quantity_id)
    if request.method == 'POST':
        size_quantity.delete()
        return redirect('adminapp:size_quantity_management')
    
    context = {'size_quantity': size_quantity}
    return render(request, 'delete_size_quantity.html', context)

def size_quantity_management(request):
    size_quantities = SizeQuantity.objects.all()
    context = {'size_quantities': size_quantities}
    return render(request, 'size_quantity_management.html', context)



# adminapp/views.py
def return_order_list(request):
    return_orders = Return.objects.all()
    return_count = Return.objects.count()
    return render(request, 'return_list.html', {'return_orders': return_orders, 'return_count': return_count})



# adminapp/views.py

def return_detail(request, return_id):
    return_obj = get_object_or_404(Return, pk=return_id)
    return_items = return_obj.return_items.all()

    return render(request, 'return_detail.html', {'return_obj': return_obj, 'return_items': return_items})




# adminapp/views.py

from django.views.generic import ListView, UpdateView
from .forms import OrderUpdateForm

class OrderListView(ListView):
    model = Order
    template_name = 'littlebubsdashboard.html'
    context_object_name = 'orders'
from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderUpdateForm

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('adminapp:order_list')  # Redirect to the order detail page
    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'order_update.html', {'form': form, 'order': order})


def user_address_list(request):
    user_addresses = UserAddress.objects.all()  # Collect all UserAddress objects
    context = {'user_addresses': user_addresses}
    return render(request, 'user_address_list.html', context)

from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.utils.timezone import now
from openpyxl import Workbook
from django.http import HttpResponse
from django.urls import reverse



def export_user_addresses_excel(request):
    user_addresses = UserAddress.objects.all()

    # Create an Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "User Addresses"
    
    # Add headers to the Excel sheet
    headers = ["First Name", "Last Name", "Place Name", "Address", "Apartment/Suite", "State/Country", "Postal/Zip", "Email", "Phone"]
    ws.append(headers)

    # Add data to the Excel sheet
    for user_address in user_addresses:
        ws.append([user_address.first_name, user_address.last_name, user_address.company_name, user_address.address, user_address.apartment_suite, user_address.state_country, user_address.postal_zip, user_address.email, user_address.phone])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="user_addresses_{now()}.xlsx'
    
    wb.save(response)

    return response


def review_list(request):
    # Retrieve a list of reviews from the database (you can use filter or any other method)
    reviews = Review.objects.all()

    # Render the HTML template with the list of reviews
    return render(request, 'review_detail.html', {'review_list': reviews})
