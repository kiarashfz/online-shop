from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone

from core.models import User

UserAdmin.list_display = ('phone', 'email', 'first_name', 'last_name', 'is_staff')
UserAdmin.search_fields = ('phone', 'first_name', 'last_name', 'email')
UserAdmin.ordering = ('phone',)
UserAdmin.fieldsets[0][1]['fields'] = ('phone', 'password')
admin.site.register(User, UserAdmin)


class BaseAdmin(admin.ModelAdmin):
    def logical_deleter(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        queryset.update(is_deleted=True)
        queryset.update(is_active=False)

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    def activate(self, request, queryset):
        queryset.update(is_active=True)

    actions = ['logical_deleter', 'deactivate', 'activate']
