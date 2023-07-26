from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Category)

class productImageAdmin(admin.StackedInline):
    model = productImage
    
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','category','price']
    inlines=[productImageAdmin]  
    
@admin.register(SizeVariant)    
class SizeVariantAdmin(admin.ModelAdmin):
        list_display=['size_name','price']
        model=SizeVariant
@admin.register(Coupon)    
class CouponAdmin(admin.ModelAdmin):
        list_display=['coupon_code','is_expired','discounted_price','minimun_amount']
        model=Coupon
        
admin.site.register(Product,ProductAdmin)

admin.site.register(productImage)

