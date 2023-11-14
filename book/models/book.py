from django.db import models

from app.decorators import autoslug


@autoslug("title")
class Book(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название")
    description = models.TextField(default="", blank=True, verbose_name="Описание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    average_rating = models.FloatField(default=0, blank=True, verbose_name="Рейтинг")

    genres = models.ManyToManyField("Genre", blank=True, verbose_name="Жанры")
    authors = models.ManyToManyField("Author", blank=True, verbose_name="Авторы")

    slug = models.SlugField(max_length=256, blank=True, null=True, verbose_name="Слаг")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
