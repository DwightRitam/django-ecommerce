from django.db import models

from django.contrib.auth.models import User

from base.models import BaseModel
from base.emails import send_account_activation
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import *
import uuid

class Profile(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token=models.CharField(max_length=100,null=True,blank=True)
    email_Otp=models.CharField(max_length=10,null=True,blank=True)
    
    def get_cart_count(self):
      return CartItem.objects.filter(cart__is_paid=False,cart__user=self.user).count()
    
    def wishlist_count(self):
      return WishListItem.objects.filter(wishlist__user=self.user).count()
    
import random
def generate_random_number():
  """Generates a 6-digit random number."""
  number = ""
  for i in range(6):
    number += str(random.randint(0, 9))
  return number    


#MEANS WHENEVER A USER OBJECT HAS BEEN CREATE ,CALL THIS SIGNAL
@receiver(post_save,sender=User)
def send_email_token(sender,instance,created, **kwargs):
    try:
        if created:
            email_token=str(uuid.uuid4())
            email_Otp=generate_random_number()
            profile=Profile.objects.create(user = instance , email_token = email_token,email_Otp=email_Otp)
            email=instance.email
            send_account_activation(email,email_token,email_Otp)
            
    except Exception as e:
        print(e)     
# by this we can distinguish which user has which cart 
class Cart(BaseModel):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_cart')
  coupon=models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank=True)
  is_paid=models.BooleanField(default=False)
  razore_pay_order_id=models.CharField(max_length=100,null=True, blank=True)
  
  
  # to get the cart total price 
  
  def get_cart_total_price(self):
    cart_items=self.cart_items.all()
    price=[]
    
    for cart_item in cart_items:
      price.append(cart_item.products.price + cart_item.size_variant.price)
      
    # print(price)  
    if self.coupon:
      return sum(price) - self.coupon.discounted_price
    return sum(price)
  
  def __str__(self):
     return self.user.username
  
# every cart model can have multiple car items 

class CartItem(BaseModel):
  cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
  products=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,related_name="cart_products")
  size_variant=models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
  
  # to get the product size j
  def get_product_size(self):
    return self.size_variant.size_name
  
  
  
  # to get the whole price 
  def get_product_price(self):
    return self.products.price + self.size_variant.price
  
  def is_item_paid(self):
    return self.cart.is_paid  
  
  def __str__(self):
     return self.products.product_name

# wishlist
# every user has wishlist that's why
class Wishlist(BaseModel):
  user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_wishlist')

  def __str__(self):
     return self.user.username
  
# every wishlist  model can have multiple wishlist items 

class WishListItem(BaseModel):
  wishlist=models.ForeignKey(Wishlist,on_delete=models.CASCADE,related_name="wishlist_items")
  products=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,related_name="wishlist_products")
  size_variant=models.ForeignKey(SizeVariant,on_delete=models.SET_NULL,null=True,blank=True)
  
  # to get the product size j
  def get_product_size(self):
    return self.size_variant.size_name
  
  
  
  # to get the whole price 
  def get_product_price(self):
    return self.products.price + self.size_variant.price

  
  def __str__(self):
     return self.products.product_name
        

class Order(BaseModel):
   user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order_cart')   
   cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="order_items")
   
   def __str__(self):
      return   self.user.username
     
     
        
        
        
        
           