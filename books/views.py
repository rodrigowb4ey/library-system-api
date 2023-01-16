from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as restfilters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book, BookCopy, Category, Publisher
from books.serializers import (
    BookCopySerializer,
    BookSerializer,
    CategorySerializer,
    PublisherSerializer,
)
from utils.api_permissions import APIPermission


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [APIPermission]
    filter_backends = [DjangoFilterBackend, restfilters.SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name']


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [APIPermission]
    filter_backends = [DjangoFilterBackend, restfilters.SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name']


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [APIPermission]
    filter_backends = [DjangoFilterBackend, restfilters.SearchFilter]
    filterset_fields = ['id', 'title', 'authors', 'category']
    search_fields = ['title', 'authors__name']

    @action(detail=True, methods=['get'], serializer_class=BookCopySerializer)
    def copies(self, request, pk=None):
        copies = BookCopy.objects.filter(book_id=pk)
        serializer = self.get_serializer(copies, many=True)

        return Response(serializer.data)


class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    permission_classes = [APIPermission]

    filter_backends = [DjangoFilterBackend, restfilters.SearchFilter]
    filterset_fields = ['id', 'book', 'date_published', 'publisher']
    search_fields = ['book__title', 'book__authors__name']
