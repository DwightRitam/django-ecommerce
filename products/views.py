from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from accounts.models import *
from django.core.mail import send_mail
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
    context={
        "categories":categories
    }
    return render(request, 'category.html',context)

def search_page(request):
    
    search=request.GET.get('search')
        
    products=Product.objects.filter(product_name__icontains=search)
        # print(search)
        # print(products)
    products_has=False
    if products.exists():
            products_has=True
    else:
            products_has=False   
    context={
            "products": products,
            "products_has":products_has,
            "search": search
            
    }   
    return render(request, 'search.html',context)

def details_page(request,slug):
    product=Product.objects.get(slug=slug)

    context={ "product" : product }
    if request.GET.get('size'):
        size=request.GET.get('size')
        
         
        price=product.get_product_price_by_size(size)
        context['selected_size']=size
        context['updated_price']=price
        
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
        messages.error(request,f'1 {products} has been added to cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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


@login_required(login_url="/sign")
def add_to_wishlist(request,uid):
    size=request.GET.get('size')
    # print(size)
    if size:
        products=Product.objects.get(uid=uid)
        
        user=request.user
        wishlist,_= Wishlist.objects.get_or_create(user=user)
        # size=request.GET.get('size')
        
        size_variant=SizeVariant.objects.get(size_name=size)
        
        wishlist_items=WishListItem.objects.create(wishlist=wishlist,products=products,size_variant=size_variant)
        # cart_items.size_variant=size_variant
       
        wishlist_items.save()
        messages.error(request,f'1 {products} has been added to wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request,'Please select a Size to proceed')
        # print('not in cart')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
@login_required(login_url="/sign")
def wishlist(request):
    try:
        wishlist_items=Wishlist.objects.get(user=request.user)
    except Exception as e:
        context={

        "wishlist_has":False,
 
    }
    
        return render(request,'wishlist.html',context)    
    
    wishlist_items=Wishlist.objects.get(user=request.user)
    wishlist_has=False
    if(request.user.profile.wishlist_count()>=1):
        wishlist_has=True
    
    else:
        
        wishlist_has=False 
    
    # print(wishlist_items)   
    context={
        
        "wishlist_items":wishlist_items,
        "wishlist_has":wishlist_has
       
        
    }
    
    return render(request,'wishlist.html',context)

@login_required(login_url="/sign")
def wish_to_cart(request,prod_uid,wishlist_uid):
    size=request.GET.get('size')
    # print(size)
    
    products=Product.objects.get(uid=prod_uid)
    wish_item=WishListItem.objects.get(uid=wishlist_uid)
    wish_item.delete()
    user=request.user
    cart,_= Cart.objects.get_or_create(user=user,is_paid=False)
       
    size_variant=SizeVariant.objects.get(size_name=size)
        
    cart_items=CartItem.objects.create(cart=cart,products=products,size_variant=size_variant)
       
    cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  
    
def remove_wishlist(request,wishlist_uid):
    try:
        wish_item=WishListItem.objects.get(uid=wishlist_uid)
        wish_item.delete()
        
    except Exception as e:
        print(e)
    # print(wishlist_uid)
        
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
        # print(payment)
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

def send_payment_successful(request,email_price,email_items,email):
    subject = 'Your Transaction has been successfully applied'
    user=request.user
    message = f'Hey {user.first_name} 👩‍💻, your order items are this:- {email_items} and yout total amount is {email_price},THANK YOU FOR SHOPPING WITH US ,HOPE WE MEET AGAIN 😊🐱‍🚀💖'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,{email})

def success(request):
    order_id=request.GET.get('order_id')
    cart=Cart.objects.get(razore_pay_order_id=order_id)
   
    #i can create order with this
    ordered=Order.objects.create(cart=cart,user=request.user)
    ordered.save()
    cart.is_paid=True
    cart.save()
    s=""
    for cart_prod in cart.cart_items.all():
        s+=cart_prod.products.product_name + ","
    #send the confirmation email
    send_payment_successful(request,cart.get_cart_total_price(),s,request.user.username)
     
    return render(request,'success.html')

@login_required(login_url="/sign")
def order(request):
    orders=Order.objects.filter(user=request.user)
    order_has=False
    if orders.exists():
        order_has=True
    else:
        order_has=False   
    context={
        "orders": orders,
        "order_has":order_has
    }   
    return render(request,'order.html',context)


    