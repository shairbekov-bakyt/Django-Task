from django.contrib import admin

from user.models import UserFavorite


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "email")

    def email(self, obj):
        return obj.user.email

    email.short_description = "Почта пользователя"
