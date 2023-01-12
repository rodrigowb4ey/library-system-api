from rest_framework import serializers

from authors.serializers import AuthorSerializer
from books.models import Book, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'cover', 'category']
