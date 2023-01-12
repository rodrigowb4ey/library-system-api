from rest_framework import serializers

from authors.models import Author
from books.serializers import BookSerializer


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']
