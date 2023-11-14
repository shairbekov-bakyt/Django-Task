from django.db import models

from user.models import User


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    book = models.ForeignKey("Book", on_delete=models.CASCADE, related_name="reviews", verbose_name="Книги")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")
    text = models.TextField(verbose_name="Описание отзыва")

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
