from rest_framework import serializers

from authors.models import Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='author-detail')

    class Meta:
        model = Author
        fields = ['id', 'name']
