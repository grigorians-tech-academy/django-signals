import asyncio

from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from .models import Post, User
from .signals import user_registered, user_registered_async


@cache_page(60 * 15)
def post_list(request):
    posts = list(
        Post.objects.values("id", "title", "content", "date")
    )
    return JsonResponse({"posts": posts}, safe=False)


def confirm_email(request, code):
    try:
        user = User.objects.get(confirmation_code=code)
        user.email_confirmed = True
        user.save()

        user_registered.send(
            sender=User,
            username=user.username,
            email=user.email,
        )

        return JsonResponse({"message": "Email confirmed."})
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "Invalid confirmation code."}, status=404
        )


async def confirm_email_async(request, code):
    try:
        user = await User.objects.aget(confirmation_code=code)
        user.email_confirmed = True
        await user.asave()

        loop = asyncio.get_event_loop()
        loop.create_task(
            user_registered_async.asend(
                sender=User,
                username=user.username,
                email=user.email,
            )
        )

        return JsonResponse({"message": "Email confirmed."})
    except User.DoesNotExist:
        return JsonResponse(
            {"message": "Invalid confirmation code."}, status=404
        )
