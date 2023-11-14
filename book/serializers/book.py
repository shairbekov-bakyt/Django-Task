from rest_framework import serializers

from book.models import Book
from book.serializers.author import AuthorSerializer
from book.serializers.genre import GenreSerializer
from book.serializers.review import ReviewSerializer


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)

    class Meta:
        model = Book
        fields = ("id", "title", "genres", "authors", "average_rating")


class BookRetrieveSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    genres = GenreSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ("id", "title", "genres", "authors", "created_date", "average_rating", "is_favorite", "reviews")

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if user and hasattr(user, "favorites") and obj.id in user.favorites.books.values_list("id", flat=True):
            return True

        return False
