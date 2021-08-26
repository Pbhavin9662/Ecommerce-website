from django.contrib import admin
from shop.models import *

# auth 
admin.site.register(Account)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
admin.site.register(Profile)


# product
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(OrderItem)