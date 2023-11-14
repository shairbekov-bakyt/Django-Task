import django_filters.rest_framework
from drf_yasg import openapi
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from book.models import Book
from book.filters import BookFilter
from book.serializers import (
    BookListSerializer, ReviewCreateSerializer,
    BookRetrieveSerializer
)


class BookViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ("title", )
    filterset_class = BookFilter
    lookup_field = 'slug'

    def get_serializer_class(self):
        methods = {
            "retrieve": BookRetrieveSerializer,
            "list": BookListSerializer,
            "review": ReviewCreateSerializer,
        }
        if self.action in methods:
            return methods[self.action]

        return super().get_serializer_class()

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Поиск книги по названию", type=openapi.TYPE_STRING),
            openapi.Parameter('date_start', openapi.IN_QUERY, description="Фильтр по дате начала", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('date_end', openapi.IN_QUERY, description="Фильтр по дате окончания", type=openapi.TYPE_STRING, format='date'),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, url_path="review", methods=["POST"])
    def review(self, request, slug, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"slug": slug, "request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_confirmed = True
        user.save()
        return Response(serializer.data)
