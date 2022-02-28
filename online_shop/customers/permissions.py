from rest_framework.permissions import BasePermission


class IsSuperUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAddressOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.customer.user
