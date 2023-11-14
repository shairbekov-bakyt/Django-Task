from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "full_name")

    def full_name(self, obj):
        return obj.get_full_name()

    full_name.short_description = "ФИО"
