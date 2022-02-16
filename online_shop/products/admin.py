from django.contrib import admin
from django.utils.html import format_html

from products.models import Discount, OffCode, Product, Category, Brand, Property


class ProductAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" width="50"/>'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ['name', 'price', 'brand', 'stock', 'category', 'final_price', 'image']


admin.site.register(Discount)
admin.site.register(OffCode)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Property)
