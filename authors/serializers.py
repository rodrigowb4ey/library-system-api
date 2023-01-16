from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['url', 'id', 'name']

    def display_value(self, instance):
        return f'{instance.name}'
