from django.db import models
from django.contrib.auth.models import AbstractUser

from user.mixins import UserEmailConfirmMixin
from user.models.user_manager import CustomUserManager


class User(AbstractUser, UserEmailConfirmMixin):
    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
