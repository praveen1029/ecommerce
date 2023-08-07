from django.contrib import admin
from ecommerce_app.views import *

# Register your models here.

admin.site.register(ProductModel)
admin.site.register(CategoryModel)
admin.site.register(CartModel)
admin.site.register(CustomerModel)