from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'adminapp'  # Namespace for the app

urlpatterns = [
       path('dashboard/', views.dashboard_view, name='dashboard'),
    path('adminlogin/', views.admin_login_view, name='admin_login'),
    path('products/', views.products_view, name='products'),
     path('admin/signup/', views.admin_signup_view, name='admin_signup'),
     path('logout/', views.logout_view, name='logout'),


     #litttlebubs
      path('littlebubsdashboard/', views.dashboard, name='littlebubsdashboard'),

 path('order/<str:order_id>/', views.order_detail, name='order_detail'),
    path('order_list', views.order_list, name='order_list'),
#littlebubs products 
path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product_list/', views.product_list, name='product_list'),
     path('products_images/', views.products_images, name='products_images'),


#littlebubs size
     path('size/add/', views.add_size, name='add_size'),
    path('size/delete/<int:size_id>/', views.delete_size, name='delete_size'),
    path('size_list', views.size_list, name='size_list'),
#littlebubs sizeand qunatity add to product

      path('size_quantity/add/', views.add_size_quantity, name='add_size_quantity'),
    path('size_quantity/delete/<int:size_quantity_id>/', views.delete_size_quantity, name='delete_size_quantity'),
    path('size_quantity_management', views.size_quantity_management, name='size_quantity_management'),
     path('edit_size_quantity/<int:size_quantity_id>/', views.edit_size_quantity, name='edit_size_quantity'),

    #littlebubs return details 
   path('return/<int:return_id>/', views.return_detail, name='return_detail'),
    path('return-orders/', views.return_order_list, name='return_list'),
#order update
     path('orders/', views.OrderListView.as_view(), name='order_lists'),
      path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),

#user details show 
      path('user_addresses/', views.user_address_list, name='user_address_list'),
    path('user_addresses/export/excel/', views.export_user_addresses_excel, name='export_user_addresses_excel'),
    #reviewList
    path('review_list/', views.review_list, name='review_list'),  

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
