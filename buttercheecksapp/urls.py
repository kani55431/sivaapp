from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


  
app_name = 'buttercheecks'  # Namespace for the app

urlpatterns = [
     path('', views.home, name='home'),
     path('shop/', views.shop, name='shop'),
path('singleshop/<int:product_id>/', views.singleshop, name='singleshop'),

      path('checkout/', views.checkout, name='checkout'),
      path('logout/', views.logout_view, name='logout'),
      path('userview/', views.user_view, name='userview'),
       path('search/', views.product_search, name='product_search'),
 path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'), 
     name='password_reset_done'),

path('reset/<uidb64>/<token>/',
auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_complete'),

    #path('signup/', views.signup, name='signup'),
 path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('cart/', views.cart, name='cart'),
path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
path('order/<int:order_id>/', views.order_details, name='order_details'),
 path('order/history/', views.order_history, name='order_history'),
 path('user/profile/', views.user_profile, name='user_profile'),
 path('products-arrivals/', views.arrivals, name='product-arrivals'),
 path('orders/', views.orders, name='orders'),
 path('manage_addresses/', views.manage_addresses, name='manage_addresses'),
    path('checkout/', views.checkout, name='checkout'),
    path('address/', views.address, name='address'),
     path('address/edit/<int:address_id>/', views.edit_address, name='edit_address'),
    # URL for deleting an address
    path('address/delete/<int:address_id>/', views.delete_address, name='delete_address'),
 path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('return-request-confirmation/', views.return_request_confirmation, name='return_request_confirmation'),
    path('return_details/<int:return_id>/', views.return_details, name='return_details'),
   path('products/<str:category>/', views.product_list_by_category, name='product_list_by_category'),
   path('about/', views.about, name='about'),
#return 
 path('order/<int:order_id>/request_return/', views.request_return, name='request_return'),
#pdf 
path('generate_invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),
 path('product/<int:product_id>/', views.product_detail, name='product_detail'),
#review
 path('create_review/<int:order_id>/', views.create_review, name='create_review'),
    path('review_submitted/', views.review_submitted, name='review_submitted'),
 path('signup-login/', views.signup_login, name='signup_login'),
    #path('login/', views.custom_login, name='login'),
       path('add_product/', views.add_product, name='add_product'),
       #path('cart/', views.cart, name='cart'),
        path('address/', views.address, name='address'),
   path('payment/<int:order_id>/', views.payment, name='payment'),
   path('success/', views.success, name='success'),
   #4.12.2023
   path('baby-swaddles/', views.swaddles_blankets, name='swaddles-and-blankets'),
  #5.12.2023
  path('clothings-jablas-rombers/', views.clothings, name='clothings'),
  path('nursing-supplies/baby-burb-cloth-sets/baby-bib cloth sets/', views.nursing_supplies, name='nursing-supplies'),
  path('babybeddings/bedding-sets/feddimg-pillows/', views.baby_beddings, name='baby-beddings'),

   #14.12.2023
  path('returnrefund', views.returnrefund, name='returnrefund'),
   #27.12.2023

    path('update_order_payment_id/', views.update_order_payment_id, name='update_order_payment_id'),
       
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
