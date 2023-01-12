from rest_framework import serializers

from authors.serializers import AuthorSerializer
from books.models import Book


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'cover']
