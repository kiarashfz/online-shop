from django.contrib import admin
from django.utils.html import format_html

from core.admin import BaseAdmin
from orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(BaseAdmin):
    def payed(self, request, queryset):
        queryset.update(pay_status=1)

    def unpayed(self, request, queryset):
        queryset.update(pay_status=0)

    ordering = ['-created', 'pay_status', 'final_price']
    list_display = ['customer', 'final_price', 'pay_status', 'off_code', 'created']
    search_fields = ['final_price']
    list_filter = ['customer', 'pay_status']
    list_per_page = 5
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'categories')
    #     }),
    #     ('Optionals', {
    #         'fields': ('country', 'description', 'discount'),
    #     }),
    # )
    # filter_vertical = ['']
    # autocomplete_fields = ['categories']
    inlines = [OrderItemInline]
    actions = ['payed', 'unpayed']


class OrderItemAdmin(BaseAdmin):
    def selected(self, request, queryset):
        queryset.update(status=0)

    def ordered(self, request, queryset):
        queryset.update(status=1)

    def image_tag(self, obj):
        return format_html('<img src="{0}" width="70"/>'.format(obj.product.image.url))

    image_tag.short_description = 'IMAGE'

    ordering = ['-created', 'status', 'final_price']
    list_display = ['product', 'count', 'customer',  'final_price', 'status', 'image_tag', 'created']
    empty_value_display = '------'
    list_editable = ['count']
    search_fields = ['product_name', 'product_brand']
    list_filter = ['customer', 'product']
    list_per_page = 5
    # fieldsets = (
    #     ('Details', {
    #         'fields': ('name', 'category', 'brand', 'image', 'properties')
    #     }),
    #     ('Marketing', {
    #         'fields': ('price', 'discount', 'liked_customers'),
    #     }),
    #     ('Inventory', {
    #         'fields': ('stock',),
    #     }),
    # )
    # filter_vertical = ['properties', 'liked_customers']
    # inlines = [ExtraImageInline]
    # auto complete for m2m or fk
    actions = ['selected', 'ordered']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
