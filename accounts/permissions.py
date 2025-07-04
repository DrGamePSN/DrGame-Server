from rest_framework.permissions import BasePermission
from django.http import HttpResponseForbidden
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




def restrict_access(*required_permissions):
    """
    دکوراتوری که دسترسی به ویو را بر اساس فیلدهای بولین مدل Employee محدود می‌کند.
    :param required_permissions: لیست فیلدهای بولین (مثل 'is_access_to_products') که باید True باشند.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(view, request, *args, **kwargs):
            # بررسی اینکه کاربر لاگین کرده و مدل Employee دارد
            if not request.user.is_authenticated:
                return HttpResponseForbidden("شما باید لاگین کنید.")

            try:
                employee = request.user.employee  # فرض می‌کنیم مدل Employee به User مرتبط است
            except AttributeError:
                return HttpResponseForbidden("کاربر معتبر نیست.")

            # بررسی همه پرمیژن‌های موردنیاز
            for permission in required_permissions:
                if not getattr(employee, permission, False):
                    return HttpResponseForbidden(f"دسترسی به این بخش ({permission}) ندارید.")

            # اگر همه پرمیژن‌ها True باشند، ویو اجرا می‌شود
            return view_func(view, request, *args, **kwargs)

        return wrapper

    # برای سازگاری با ویوهای کلاسی
    return method_decorator(decorator, name='dispatch')
