from django.contrib import admin
from django.utils.html import format_html

from core.admin import BaseAdmin
from products.models import Discount, OffCode, Product, Category, Brand, Property, ExtraImage


class ProductInline(admin.StackedInline):
    model = Product
    extra = 1


class ExtraImageInline(admin.StackedInline):
    model = ExtraImage
    extra = 1


class ExtraImageAdmin(BaseAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{0}" width="70"/>'.format(obj.image.url))

    image_tag.short_description = 'IMAGE'

    list_display = ['product', 'image_tag']
    search_fields = ['product__name']
    list_filter = ['product']
    list_per_page = 5


class DiscountAdmin(BaseAdmin):
    ordering = ['value', 'expire']
    list_display = ['__str__', 'type', 'value', 'max_amount', 'expire']
    list_display_links = ['__str__']
    list_editable = ['value', 'max_amount']
    search_fields = ['__str__', 'value', 'expire']
    list_filter = ['value']
    list_per_page = 5
    fieldsets = (
        (None, {
            'fields': ('type', 'value')
        }),
        ('Optionals', {
            'fields': ('max_amount', 'expire'),
        }),
    )
    empty_value_display = '------'


class OffCodeAdmin(BaseAdmin):
    ordering = ['value', 'expire']
    list_display = ['__str__', 'type', 'value', 'max_amount', 'expire']
    list_display_links = ['__str__']
    list_editable = ['value', 'max_amount']
    search_fields = ['__str__', 'value', 'expire']
    list_filter = ['value']
    list_per_page = 5
    fieldsets = (
        (None, {
            'fields': ('type', 'value', 'code')
        }),
        ('Optionals', {
            'fields': ('min_buy', 'max_amount', 'expire', 'usable_count'),
        }),
    )
    empty_value_display = '------'


class ProductAdmin(BaseAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{0}" width="70"/>'.format(obj.image.url))

    image_tag.short_description = 'IMAGE'

    ordering = ['name', 'category', 'brand']
    list_display = ['name', 'stock', 'price', 'discount',  'final_price', 'image_tag']
    empty_value_display = '------'
    list_editable = ['stock', 'discount']
    search_fields = ['name', 'category_name', 'discount__value', 'brand_name', 'stock', 'price', 'final_price']
    list_filter = ['category', 'brand', 'discount']
    list_per_page = 5
    fieldsets = (
        ('Details', {
            'fields': ('name', 'category', 'brand', 'image', 'properties')
        }),
        ('Marketing', {
            'fields': ('price', 'discount'),
        }),
        ('Inventory', {
            'fields': ('stock',),
        }),
    )
    filter_vertical = ['properties']
    inlines = [ExtraImageInline]
    # auto complete for m2m or fk


class PropertyAdmin(BaseAdmin):
    ordering = ['key', 'value']
    list_display = ['key', 'value']
    list_editable = ['value']
    search_fields = ['key', 'value']
    list_filter = ['key']
    list_per_page = 10
    empty_value_display = '------'


class CategoryAdmin(BaseAdmin):
    ordering = ['name']
    list_display = ['name', 'parent', 'discount']
    list_editable = ['discount']
    search_fields = ['name', 'parent_name', 'discount__value']
    list_filter = ['parent', 'discount']
    list_per_page = 5
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Optionals', {
            'fields': ('parent', 'discount'),
        }),
    )
    autocomplete_fields = ['parent']
    empty_value_display = '------'
    inlines = [ProductInline]


class BrandAdmin(BaseAdmin):
    @admin.display(description='NAME')
    def colored_name(self, obj):
        return format_html(
            '<span style="color: #{};">{}</span>',
            '0000FF',
            obj.name,
        )
    # fields = (('name', 'country'), 'description', 'discount')
    ordering = ['name', 'country']
    list_display = ['name', 'country', 'discount']
    list_editable = ['country', 'discount']
    search_fields = ['name', 'country', 'discount__value']
    list_filter = ['country']
    list_per_page = 5
    fieldsets = (
        (None, {
            'fields': ('name', 'categories')
        }),
        ('Optionals', {
            'fields': ('country', 'description', 'discount'),
        }),
    )
    filter_vertical = ['categories']
    # autocomplete_fields = ['categories']
    inlines = [ProductInline]


admin.site.register(Discount, DiscountAdmin)
admin.site.register(OffCode, OffCodeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(ExtraImage, ExtraImageAdmin)
