#main/urls.py

from django.urls import path 
from .views import *
from products.views import *
urlpatterns = [
    path("", index, name="index"),
    
    path('send_email/', send_email , name="send_email"),
    path('sign/email_verification/<email_token>/', email_verification , name="email_verification"),
    # path('activate/<email_token>/', activate_email , name="activate_email"),
     
]