from django.contrib import admin
from django.urls import path, include  # Import the include function
from django.contrib.auth import views as auth_views  # Import Django's authentication views
urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('', include('buttercheecksapp.urls', namespace='buttercheecksapp')),

 
   path('adminapp/', include('adminapp.urls')), 
   path('', include('django.contrib.auth.urls')),
]
