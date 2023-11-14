from django.contrib import admin

from book.models import Book, Review


class BookReviewInline(admin.TabularInline):
    model = Review
    max_num = 3


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "average_rating", "created_date")
    list_filter = ("average_rating", "created_date")
    inlines = [BookReviewInline]
