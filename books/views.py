from rest_framework import permissions, viewsets

from books.models import Book
from books.serializers import BookSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
