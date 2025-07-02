from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return hasattr(request.user, 'customer') or hasattr(request.user, 'business_customer')


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employee')


class IsMainManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'main_manger')


class IsSuperuserOrHasRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return (hasattr(request.user, 'customer') or
                hasattr(request.user, 'business_customer') or
                 hasattr(request.user, 'employee') or
                 hasattr(request.user, 'main_manager'))
