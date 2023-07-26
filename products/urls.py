#main/urls.py

from .views import *
from django.urls import path 
urlpatterns = [
    path("", index, name="index"),
    path("get_categories/<category>", get_categories, name="get_categories"),
    path("<slug>/", details_page, name="details_page"),
    path("cart/remove_Cart/<cart_item_uid>",remove_Cart,name="remove_Cart"),
    path("cart/success/",success,name="success"),
    path("remove_coupon/<uid>",remove_coupon,name="remove_coupon"),
]