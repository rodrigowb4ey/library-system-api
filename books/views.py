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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'], serializer_class=BookCopySerializer)
    def copies(self, request, pk=None):
        copies = BookCopy.objects.filter(book_id=pk)
        serializer = self.get_serializer(copies, many=True)

        return Response(serializer.data)
