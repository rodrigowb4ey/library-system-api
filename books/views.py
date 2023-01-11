from django.shortcuts import render

from rest_framework import viewsets, permissions

from books.models import Book
from books.serializers import BookSerializer

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
