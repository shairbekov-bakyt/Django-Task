from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=256, verbose_name="ФИО")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
