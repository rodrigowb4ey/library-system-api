from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as restfilters
from rest_framework import permissions, viewsets

from authors.models import Author
from authors.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, restfilters.SearchFilter]
    filterset_fields = ['id', 'name']
    search_fields = ['name']
