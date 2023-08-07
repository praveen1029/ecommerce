from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CategoryModel(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name

class CustomerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    user_age = models.IntegerField()
    user_dob = models.DateField()
    user_gender = models.CharField(max_length=10)
    user_addr = models.CharField(max_length=100)
    user_phno = models.IntegerField()
    photo = models.ImageField(upload_to="image/",null=True)

    def __str__(self):
        return self.user
    

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE,null=True)
    pr_name = models.CharField(max_length=100)
    pr_cost = models.IntegerField(default=0)
    pr_discount = models.IntegerField(default=0)
    pr_discost = models.IntegerField(null=True)
    pr_brand = models.CharField(max_length=100,null=True)
    pr_rating = models.IntegerField(null=True)
    pr_colour = models.CharField(max_length=50,null=True)
    pr_description = models.CharField(max_length=250,null=True)
    manufacture_date = models.DateField(null=True)
    pr_mimage = models.ImageField(upload_to="image/",null=True)
    pr_simage1 = models.ImageField(upload_to="image/",null=True)
    pr_simage2 = models.ImageField(upload_to="image/",null=True)
    pr_simage3 = models.ImageField(upload_to="image/",null=True)

    def __str__(self):
        return self.pr_name

class CartModel(models.Model):
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(CustomerModel,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.product
