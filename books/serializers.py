from rest_framework import serializers

from authors.models import Author
from authors.serializers import AuthorSerializer
from books.models import Book, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True, queryset=Author.objects.all(), slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'cover', 'category']
