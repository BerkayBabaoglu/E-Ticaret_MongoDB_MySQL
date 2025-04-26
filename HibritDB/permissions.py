from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'customer'

class IsSupplier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'supplier'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin' 