from django.shortcuts import get_object_or_404
from rest_framework import serializers

from book.models import Review, Book
from user.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = ("id", "rating", "text", "user")


class ReviewCreateSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ("rating", "text")

    def create(self, validated_data):
        user = self.context["request"].user
        book_slug = self.context["slug"]
        book = get_object_or_404(Book, slug=book_slug)
        return Review.objects.create(**validated_data, user=user, book=book)
