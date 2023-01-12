from rest_framework import serializers

from authors.models import Author
from books.models import Book, BookCopy, Category, Publisher


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class PublisherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Publisher
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


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BookCopy
        fields = ['id', 'title', 'date_published', 'book', 'publisher']

    def get_title(self, object):
        return object.__str__()
