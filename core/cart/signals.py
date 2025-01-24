from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .cart import CartSession
from .models import CartItem
from shop.models import Product, StatusType
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    cart = CartSession(request.session)
    cart.sync_cart_items_from_db(user)


@receiver(user_logged_out)
def pre_logout(sender, user, request, **kwargs):
    cart = CartSession(request.session)
    cart.merge_session_cart_in_db(user)


@receiver(post_delete, sender=Product)
def remove_deleted_product_from_cart(sender, instance, **kwargs):
    sessions = Session.objects.all()
    for session in sessions:
        data = session.get_decoded()  # Decode the session data
        if "cart" in data:
            # Filter out the deleted product from the cart
            data["cart"]["items"] = [
                item for item in data["cart"]["items"]
                if item["product_id"] != str(instance.id)
            ]
            session.session_data = SessionStore().encode(data)  # Encode updated data
            session.save()  # Save the session

    CartItem.objects.filter(product=instance).delete()


@receiver(post_save, sender=Product)
def remove_unpublished_product_from_cart(sender, instance, **kwargs):
    if instance.status != StatusType.publish.value:
        sessions = Session.objects.all()
        for session in sessions:
            data = session.get_decoded()  # Decode the session data
            if "cart" in data:
                # Filter out the unpublished product from the cart
                data["cart"]["items"] = [
                    item for item in data["cart"]["items"]
                    if item["product_id"] != str(instance.id)
                ]
                session.session_data = SessionStore().encode(data)  # Encode updated data
                session.save()  # Save the session

        CartItem.objects.filter(product=instance).delete()
