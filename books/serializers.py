from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from authors.models import Author
from authors.serializers import AuthorSerializer
from books.models import Book, BookCopy, Category, Publisher


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'id', 'name']


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publisher
        fields = ['url', 'id', 'name']


class BookSerializer(FlexFieldsModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'authors', 'category']
        expandable_fields = {'authors': (AuthorSerializer, {'many': True})}


class BookCopySerializer(FlexFieldsModelSerializer):
    publisher = serializers.SlugRelatedField(
        queryset=Publisher.objects.all(), slug_field='name'
    )

    class Meta:
        model = BookCopy
        fields = [
            'url',
            'id',
            'book',
            'date_published',
            'publisher',
            'cover',
        ]
        expandable_fields = {'book': BookSerializer}
