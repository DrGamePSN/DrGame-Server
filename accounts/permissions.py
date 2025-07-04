from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from django.http import HttpResponseForbidden, HttpResponse
from django.utils.decorators import method_decorator
from functools import wraps


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


def restrict_access(user_boolean_field):
    def decorator(view_class):
        original_initial = view_class.initial

        @wraps(view_class)
        def new_initial(self, request, *args, **kwargs):
            employee = request.user.employee
            if not getattr(employee, user_boolean_field, False):
                raise PermissionDenied(f"Access denied: {user_boolean_field} is False or not present.")
            return original_initial(self, request, *args, **kwargs)

        view_class.initial = new_initial
        return view_class

    return decorator