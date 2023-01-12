from rest_framework import serializers

from authors.models import Author
from books.models import Book, BookCopy, Category, Publisher


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = ['id', 'name']


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='publisher-detail')

    class Meta:
        model = Publisher
        fields = ['id', 'name']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='book-detail')
    authors = serializers.SlugRelatedField(
        many=True, queryset=Author.objects.all(), slug_field='name'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'category']


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='bookcopy-detail')
    publisher = serializers.SlugRelatedField(
        queryset=Publisher.objects.all(), slug_field='name'
    )
    book = serializers.HyperlinkedRelatedField(
        view_name='book-detail', queryset=Book.objects.all()
    )

    class Meta:
        model = BookCopy
        fields = ['id', 'book', 'date_published', 'publisher', 'cover']
        depth = 3
