from django.db import models

from  base.models import BaseModel
# Create your models here.
from django.utils.text import slugify
class Category(BaseModel):
    category_name=models.CharField(max_length=100)
    gender_category=models.CharField(max_length=20,null=True)
    slug=models.SlugField(unique=True,null=True,blank=True)
    category_image=models.ImageField(upload_to="categories")
    price=models.IntegerField(default=0)
    product_name=models.CharField(max_length=100,null=True)
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.category_name
        
    

class SizeVariant(BaseModel):
    # for shoes there will be different types of size variants and for tshirt there will be different types of size variants
    # type_of_size=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category_variant")
    size_name=models.CharField(max_length=20,null=True)  
    price=models.IntegerField(default=0)  
    
    def __str__(self):
        return self.size_name
    
class Product(BaseModel):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True,null=True,blank=True)
    #we are bringing the category from the Category object
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="products_category")
    price=models.IntegerField()
    product_description=models.TextField()
    # suppose a category many types of sizes,that's why manytomanyfiels
    size_variant=models.ManyToManyField(SizeVariant)
    # is someone add this product then it's count will increase

   
        
    def save(self, *args, **kwargs):
        self.slug=slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.product_name
    
    
    def get_product_price_by_size(self,size):
        return self.price + SizeVariant.objects.get(size_name=size).price
    
    
#every product can have multiple images
class productImage(BaseModel):
    product =models.ForeignKey(Product,on_delete=models.CASCADE,related_name="product_images")
    image=models.ImageField(upload_to="product")   
    
class Coupon(BaseModel):
    coupon_code=models.CharField(max_length=20)
    is_expired=models.BooleanField(default=False)
    discounted_price=models.IntegerField(default=200)
    minimun_amount=models.IntegerField(default=1500)