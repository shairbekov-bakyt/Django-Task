from datetime import datetime, time

from django_filters import rest_framework as filters

from book.models import Book, Author, Genre


class BookFilter(filters.FilterSet):
    authors = filters.CharFilter(method='filter_authors')
    genres = filters.CharFilter(method='filter_genres')
    date_start = filters.DateFilter(method="filter_by_date_start")
    date_end = filters.DateFilter(method="filter_by_date_end")

    def filter_authors(self, queryset, name, value):
        author_ids = value.split(',')
        return queryset.filter(authors__id__in=author_ids).distinct() if author_ids else queryset

    def filter_genres(self, queryset, name, value):
        genres_ids = value.split(',')
        return queryset.filter(genres__id__in=genres_ids).distinct() if genres_ids else queryset

    def filter_by_date_start(self, queryset, name, value):
        first_hours = time(00, 00)
        return queryset.filter(created_at__gte=datetime.combine(value, first_hours)) if value else queryset

    def filter_by_date_end(self, queryset, name, value):
        last_hours = time(23, 59)
        return queryset.filter(created_at__lte=datetime.combine(value, last_hours)) if value else queryset

    class Meta:
        model = Book
        fields = ['authors', 'genres']
