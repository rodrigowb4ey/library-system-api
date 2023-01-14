from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['url', 'id', 'title', 'authors', 'category']

    def get_or_create_author_instance(self, author_data=None):
        if author_data:
            author_obj, created = Author.objects.get_or_create(
                name=author_data['name']
            )

            return author_obj

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')

        author_instances = [
            self.get_or_create_author_instance(author_data)
            for author_data in authors_data
        ]

        book = Book(
            title=validated_data.pop('title'),
            category=validated_data.pop('category'),
        )
        book.save()

        for author in author_instances:
            book.authors.add(author)

        return book

    def update(self, object, validated_data):
        authors_data = validated_data.pop('authors')

        author_instances = [
            self.get_or_create_author_instance(author_data)
            for author_data in authors_data
        ]

        object.title = validated_data.pop('title')
        object.category = validated_data.pop('category')

        object.authors.set(author_instances)
        object.save(update_fields=['title', 'category'])

        return object


class BookCopySerializer(serializers.HyperlinkedModelSerializer):
    publisher = serializers.SlugRelatedField(
        queryset=Publisher.objects.all(), slug_field='name'
    )
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book = BookSerializer(read_only=True)

    class Meta:
        model = BookCopy
        fields = [
            'url',
            'id',
            'book_id',
            'book',
            'date_published',
            'publisher',
            'cover',
        ]

    def create(self, validated_data):
        book_id = validated_data.pop('book_id').pk

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise ValidationError(
                {'detail': 'Book does not exist in database.'}
            )

        args = {key: value for key, value in validated_data.items()}

        book_copy = BookCopy.objects.create(book=book, **args)

        return book_copy

    def update(self, object, validated_data):
        new_book_id = validated_data.pop('book_id').pk

        try:
            new_book = Book.objects.get(pk=new_book_id)
        except Book.DoesNotExist:
            raise ValidationError(
                {'detail': 'Book does not exist in database.'}
            )

        keys = []

        for key, value in validated_data.items():
            setattr(object, key, value)
            keys.append(key)

        object.book = new_book
        object.save(update_fields=keys)

        return object
