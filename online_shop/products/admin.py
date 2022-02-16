from django.contrib import admin

from products.models import Discount, OffCode, Product, Category, Brand, Property

admin.site.register(Discount)
admin.site.register(OffCode)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Property)
