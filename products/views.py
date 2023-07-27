from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *

import razorpay
def index(request):
    categories=Category.objects.all()
    context={
        "categories":categories
    }
    return render(request, 'index.html',context)

def get_by_genders(request,gender):
    categories=Category.objects.filter(gender_category=gender)
    # print(categories)
    context={
        "categories":categories,
        "gender":gender
    }
    return render(request, 'gendor.html',context)

def get_categories(request,category_type):
    categories=Category.objects.filter(category_name=category_type)
    for category in categories:
        for product in category.products_category.all():
            print(product.product_name)
            print(product.slug)
            print(product.category)
            print(category.category_image)
    context={
        "categories":categories
    }
    return render(request, 'category.html',context)
def details_page(request,slug):
    product=Product.objects.get(slug=slug)

    context={ "product" : product }
    if request.GET.get('size'):
        size=request.GET.get('size')
        # print(size)
        size_variant=SizeVariant.objects.get(size_name=size)
        cart_items=CartItem.objects.filter(products=product,size_variant=size_variant)
        
        already_exists=False
        if cart_items.exists():
            already_exists=True
            # print('already exists')
        else:
            already_exists=False
            # print('not exists')    
        price=product.get_product_price_by_size(size)
        context['selected_size']=size
        context['updated_price']=price
        context['already_exists']=already_exists
        
        # print(price)
    
    return render(request, 'product_details.html',context=context)

@login_required(login_url="/sign")
def add_to_cart(request,uid):
    size=request.GET.get('size')
    # print(size)
    if size:
        products=Product.objects.get(uid=uid)
        
        user=request.user
        cart,_= Cart.objects.get_or_create(user=user,is_paid=False)
        # size=request.GET.get('size')
        size_variant=SizeVariant.objects.get(size_name=size)
        
        cart_items=CartItem.objects.create(cart=cart,products=products,size_variant=size_variant)
        # cart_items.size_variant=size_variant
       
        cart_items.save()
        return redirect('/cart')
    else:
        messages.error(request,'Please select a Size to proceed')
        # print('not in cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def remove_Cart(request,cart_item_uid):
    try:
        cart_item=CartItem.objects.get(uid=cart_item_uid)
        cart_item.delete()
        
    except Exception as e:
        print(e)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from django.conf import settings

@login_required(login_url="/sign")
def cart(request):
    cart_items=None
    try:
        cart_items=Cart.objects.get(is_paid=False,user=request.user)
    except Exception as e:
        context={

        "cart_has":False,
 
    }
    
        return render(request, 'cart.html',context)    
    cart_has=False
    if(request.user.profile.get_cart_count()>=1):
        cart_has=True
    
    else:
        
        cart_has=False    
        
    if request.method=='POST':
        coupon=request.POST.get('coupon')
        
        coupon_obj=Coupon.objects.filter(coupon_code__icontains= coupon)
        # print(coupon_obj)
        if not coupon_obj.exists():
            messages.error(request,f'there is no coupon with code '+coupon)
             # print('not in cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_items.coupon:
            messages.warning(request,'coupon already exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart_items.get_cart_total_price() < coupon_obj[0].minimun_amount:
            messages.warning(request,f'Amount should be greater then {coupon_obj[0].minimun_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon_obj[0].is_expired:
            messages.warning(request,'Coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        cart_items.coupon=coupon_obj[0]
        cart_items.save()
        messages.success(request,'coupon applied')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
      
    
    # payment 
    if cart_items:
        after_shipping=cart_items.get_cart_total_price()+100
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        amount=0
        if(request.user.profile.get_cart_count()>=1):
            amount=after_shipping
        else:
            amount=10    
        payment=client.order.create({'amount': amount * 100,'currency': "INR", 'payment_capture':1})
        
        cart_items.razore_pay_order_id=payment['id']
        cart_items.save()
        print(payment)
    # payment=None
    
    context={
        
        "cart_items":cart_items,
        "cart_has":cart_has,
        "after_shipping":after_shipping,
        'payment':payment
        
    }
    
    return render(request, 'cart.html',context)    


def remove_coupon(request,uid):
    cart=Cart.objects.get(uid=uid)
    cart.coupon=None
    cart.save()
    messages.success(request,'coupon applied')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


def success(request):
    order_id=request.GET.get('order_id')
    cart=Cart.objects.get(razore_pay_order_id=order_id)
    cart.is_paid=True
    cart.save()
    return render(request,'success.html')