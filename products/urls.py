#main/urls.py

from .views import *
from django.urls import path 
urlpatterns = [
    path("", index, name="index"),
    path("get_categories/<category_type>", get_categories, name="get_categories"),
    
    path("get_by_genders/<gender>", get_by_genders, name="get_by_genders"),
    path("<slug>/", details_page, name="details_page"),
    path("user/orders/", order, name="order"),
    path("cart/remove_Cart/<cart_item_uid>",remove_Cart,name="remove_Cart"),
    path("cart/remove_wishlist/<wishlist_uid>",remove_wishlist,name="remove_wishlist"),
    path("cart/wish_to_cart/<prod_uid>/<wishlist_uid>",wish_to_cart,name="wish_to_cart"),
    path("cart/success/",success,name="success"),
    path("remove_coupon/<uid>",remove_coupon,name="remove_coupon"),
]