from django.contrib import admin
from django.utils.html import format_html

from core.admin import BaseAdmin
from customers.models import Customer, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class CustomerAdmin(BaseAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{0}" width="70"/>'.format(obj.image.url))

    image_tag.short_description = 'IMAGE'

    ordering = ['user']
    list_display = ['user', 'image_tag']
    search_fields = ['user_first_name', 'user_last_name', 'user_phone', 'user_email']
    list_per_page = 5
    fieldsets = (
        ('Personal Info', {
            'fields': ('user', )
        }),
        ('Optionals', {
            'fields': ('image', ),
        }),
    )
    # filter_vertical = ['product_set']
    # autocomplete_fields = ['user']
    inlines = [AddressInline]


class AddressAdmin(BaseAdmin):
    ordering = ['province']
    list_display = ['customer', 'province', 'city', 'area', 'area', 'avenue', 'no', 'postal_code']
    list_editable = ['province', 'city', 'area', 'area', 'avenue', 'no', 'postal_code']
    # search_fields = ['customer']
    list_filter = ['province', 'city', 'area']
    list_per_page = 5
    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'categories')
    #     }),
    #     ('Optionals', {
    #         'fields': ('country', 'description', 'discount'),
    #     }),
    # )
    # filter_vertical = ['categories']
    # autocomplete_fields = ['categories']
    # inlines = [ProductInline]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
