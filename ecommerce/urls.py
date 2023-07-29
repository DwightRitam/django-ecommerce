"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path 

from accounts.views import *
from products.views import cart,add_to_cart,search_page,wishlist,add_to_wishlist
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page , name="login_page"),
    path('sign/', signin_page , name="signin_page"),
    path('logout', logout_page , name="logout_page"),
    path('searchpage/query', search_page , name="search_page"),
    path('wishlist', wishlist , name="wishlist"),
    path('cart', cart , name="cart"),
    path("add_to_cart/<uid>",add_to_cart,name="add_to_cart"),
    path("add_to_wishlist/<uid>",add_to_wishlist,name="add_to_wishlist"),
    path('', include("products.urls")),
    path('', include("accounts.urls")),
    path("__reload__/", include("django_browser_reload.urls"))
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns+=staticfiles_urlpatterns()  

#for vercel
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
