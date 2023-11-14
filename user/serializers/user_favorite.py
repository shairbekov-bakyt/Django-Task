from rest_framework import serializers

from book.models import Book


class UserFavoriteSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def validate_book_id(self, value):
        book = Book.objects.filter(pk=value).first()
        if not book:
            raise serializers.ValidationError("Книга с айди {value} не найден")

        return value
