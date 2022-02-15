from django.contrib import admin

from customers.models import Customer, Address

admin.site.register(Customer)
admin.site.register(Address)
