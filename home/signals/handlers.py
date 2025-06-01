# accounts/signals.py
# from django.db.models.signals import user_logged_in
from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from home.models import Cart, CartItem


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    """Merge session cart into user cart on login"""
    # 1. Ensure session exists
    if not hasattr(request, 'session'):
        return

    if not request.session.session_key:
        request.session.create()

    # 2. Find session cart
    try:
        session_cart = Cart.objects.get(
            session_key=request.session.session_key,
            is_deleted=False
        )
    except Cart.DoesNotExist:
        return

    # 3. Get or create user cart
    user_cart, _ = Cart.objects.get_or_create(
        user=user,
        is_deleted=False,
        defaults={'session_key': None}
    )

    # 4. Process items in transaction
    with transaction.atomic():
        for session_item in session_cart.cart_items.filter(is_deleted=False):
            # Try to find matching item in user cart
            user_item = user_cart.cart_items.filter(
                product=session_item.product,
                is_deleted=False
            ).first()

            if user_item:
                # Merge quantities
                user_item.quantity += session_item.quantity
                user_item.save()
                session_item.delete()
            else:
                # Transfer item to user cart
                session_item.cart = user_cart
                session_item.save()

        # 5. Clean up session cart
        session_cart.delete()


# @receiver(user_logged_in)
# def merge_carts(sender, request, user, **kwargs):
#     if request.session.session_key:
#         try:
#             session_cart = Cart.objects.get(session_key=request.session.session_key)
#             user_cart, created = Cart.objects.get_or_create(user=request.user)
#
#             for item in session_cart.cart_items.all():
#
#                 try:
#                     user_cart_item = user_cart.cart_items.get(product=item.product, is_deleted=False)
#                     user_cart_item.quantity += item.quantity
#                     user_cart_item.save()
#                     item.delete()
#                 except CartItem.DoesNotExist:
#                     item.cart = user_cart
#                     item.save()
#                     CartItem.objects.filter(pk=item.pk).update(cart=user_cart)
#
#             session_cart.delete()
#
#         except Cart.DoesNotExist:
#             print('hi')
