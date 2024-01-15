import asyncio

from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver
from django.utils.crypto import get_random_string

from .models import Post, User


@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def invalidate_cache(sender, **kwargs):
    cache.clear()


@receiver(post_save, sender=User)
def send_confirmation_email(sender, instance, **kwargs):
    if not instance.confirmation_email_sent:
        print("Sending confirmation email...")
        instance.confirmation_email_sent = True
        instance.confirmation_code = get_random_string(length=32)
        instance.save()


user_registered = Signal()


@receiver(user_registered)
def send_welcome_email(sender, **kwargs):
    print("Sending welcome email...")
    username = kwargs.get("username")
    email = kwargs.get("email")
    if username and email:
        print(f"Welcome {username}! We sent you an email to {email}.")


user_registered_async = Signal()


@receiver(user_registered_async)
async def async_send_welcome_email(sender, **kwargs):
    print("Sending welcome email...")
    username = kwargs.get("username")
    email = kwargs.get("email")
    if username and email:
        print(f"Welcome {username}! We sent you an email to {email}.")
    await asyncio.sleep(5)
    print("Welcome email sent!")
