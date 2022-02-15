from django.contrib import admin

from products.models import Discount, OffCode, Product, Category

admin.site.register(Discount)
admin.site.register(OffCode)
admin.site.register(Product)
admin.site.register(Category)
