from rest_framework import serializers

from authors.models import Author
from books.models import Book, BookCopy, Category, Publisher


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'id', 'name']


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publisher
        fields = ['url', 'id', 'name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = serializers.SlugRelatedField(
        many=True, queryset=Author.objects.all(), slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'authors', 'category']


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    publisher = serializers.SlugRelatedField(
        queryset=Publisher.objects.all(), slug_field='name'
    )
    book = serializers.HyperlinkedRelatedField(
        view_name='book-detail', queryset=Book.objects.all()
    )

    class Meta:
        model = BookCopy
        fields = ['url', 'id', 'book', 'date_published', 'publisher', 'cover']
        depth = 3
