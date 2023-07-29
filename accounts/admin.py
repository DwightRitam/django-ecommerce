from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Profile)

@admin.register(Cart)    
class CartAdmin(admin.ModelAdmin):
        list_display=['user','is_paid']
        model=Cart


@admin.register(CartItem)    
class CartItemAdmin(admin.ModelAdmin):
        list_display=['cart','products','size_variant']
        model=CartItem
        
@admin.register(Wishlist)    
class WishlistAdmin(admin.ModelAdmin):
        list_display=['user']
        model=Wishlist


@admin.register(WishListItem)    
class WishListItemAdmin(admin.ModelAdmin):
        list_display=['wishlist','products','size_variant']
        model=WishListItem

@admin.register(Order)    
class OrderAdmin(admin.ModelAdmin):
        list_display=['user','cart']
        model=Order


