from django.contrib import admin

from main.models import Post, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "id",
        "confirmation_email_sent",
        "email_confirmed",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
