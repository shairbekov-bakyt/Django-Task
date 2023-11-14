from django.db import models

from book.models import Book
from user.models.user import User


class UserFavorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="favorites", verbose_name="Пользователь")
    books = models.ManyToManyField(Book, blank=True, verbose_name="Книги")

    class Meta:
        verbose_name = "Избранная книги"
        verbose_name_plural = "Избранные книги"
