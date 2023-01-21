import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from authors.models import Author

from .factories import AuthorFactory


@pytest.mark.django_db
class TestAuthorEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('author-list')
        self.super_user = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='password',
        )
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password',
            is_staff=True,
        )
        self.common_user = User.objects.create_user(
            username='nonadmin',
            email='nonadmin@example.com',
            password='password',
        )

    def test_get_authors_unauthenticated(self):
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_authors_authenticated(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_author_by_id_unauthenticated(self):
        author = AuthorFactory()
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(author.pk)
        assert data['name'] == author.name

    def test_get_author_by_id_authenticated(self):
        self.client.force_authenticate(self.common_user)
        author = AuthorFactory()
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(author.pk)
        assert data['name'] == author.name

    def test_post_author_unauthenticated(self):
        response = self.client.post(self.url, {'name': 'John Doe'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_author_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.post(self.url, {'name': 'John Doe'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_author_authenticated_admin(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(self.url, {'name': 'John Doe'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'John Doe'

    def test_post_author_authenticated_superuser(self):
        self.client.force_authenticate(self.super_user)
        response = self.client.post(self.url, {'name': 'John Doe'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'John Doe'

    def test_put_author_unauthenticated(self):
        author = AuthorFactory()
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.put(
            url, content_type='application/json', data={'name': 'Dohn Joe'}
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_author_authenticated_common_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.put(
            url, content_type='application/json', data={'name': 'Dohn Joe'}
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_author_authenticated_admin_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.admin_user)
        request_data = dict(name='Dohn Joe')
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.put(
            url, content_type='application/json', data=json.dumps(request_data)
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == str(author.pk)
        assert response.data['name'] == 'Dohn Joe'

    def test_put_author_authenticated_super_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.super_user)
        request_data = dict(name='Dohn Joe')
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.put(
            url, content_type='application/json', data=json.dumps(request_data)
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == str(author.pk)
        assert response.data['name'] == 'Dohn Joe'

    def test_patch_author_unauthenticated(self):
        author = AuthorFactory()
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.patch(
            url, content_type='application/json', data={'name': 'Dohn Joe'}
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_author_authenticated_common_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.patch(
            url, content_type='application/json', data={'name': 'Dohn Joe'}
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_author_authenticated_admin_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.admin_user)
        request_data = dict(name='Dohn Joe')
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.patch(
            url, content_type='application/json', data=json.dumps(request_data)
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == str(author.pk)
        assert response.data['name'] == 'Dohn Joe'

    def test_patch_author_authenticated_super_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.super_user)
        request_data = dict(name='Dohn Joe')
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.patch(
            url, content_type='application/json', data=json.dumps(request_data)
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['id'] == str(author.pk)
        assert response.data['name'] == 'Dohn Joe'

    def test_delete_author_unauthenticated(self):
        author = AuthorFactory()
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_author_authenticated_common_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_author_authenticated_admin_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.admin_user)
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Author.objects.filter(pk=author.pk).exists()

    def test_delete_author_authenticated_super_user(self):
        author = AuthorFactory()
        self.client.force_authenticate(self.super_user)
        url = reverse('author-detail', kwargs={'pk': author.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Author.objects.filter(pk=author.pk).exists()
