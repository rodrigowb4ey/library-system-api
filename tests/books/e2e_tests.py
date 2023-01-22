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

from books.models import Book

from ..authors.factories import AuthorFactory
from ..categories.factories import CategoryFactory
from .factories import BookFactory


@pytest.mark.django_db
class TestBookEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('book-list')
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

    def test_get_books_unauthenticated(self):
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_books_authenticated(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_book_by_id_unauthenticated(self):
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(book.pk)
        assert data['title'] == book.title

    def test_get_book_by_id_authenticated(self):
        self.client.force_authenticate(self.common_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(book.pk)
        assert data['title'] == book.title

    def test_post_book_unauthenticated(self):
        author = AuthorFactory()
        category = CategoryFactory()
        response = self.client.post(
            self.url,
            {
                'title': 'BookTest',
                'authors': [str(author.pk)],
                'category': category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_book_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        author = AuthorFactory()
        category = CategoryFactory()
        response = self.client.post(
            self.url,
            {
                'title': 'BookTest',
                'authors': [str(author.pk)],
                'category': category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_book_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        author = AuthorFactory()
        category = CategoryFactory()
        response = self.client.post(
            self.url,
            {
                'title': 'BookTest',
                'authors': [str(author.pk)],
                'category': category.name,
            },
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.data['title'] == 'BookTest'
        assert response.data['authors'] == [author.pk]
        assert response.data['category'] == category.name

    def test_post_book_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        author = AuthorFactory()
        category = CategoryFactory()
        response = self.client.post(
            self.url,
            {
                'title': 'BookTest',
                'authors': [str(author.pk)],
                'category': category.name,
            },
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.data['title'] == 'BookTest'
        assert response.data['authors'] == [author.pk]
        assert response.data['category'] == category.name

    def test_put_book_unauthenticated(self):
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.put(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_book_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.put(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_book_super_user(self):
        self.client.force_authenticate(self.super_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.put(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'NewTitleBookTest'
        assert response.data['authors'] == [new_author.pk]
        assert response.data['category'] == new_category.name

    def test_put_book_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.put(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'NewTitleBookTest'
        assert response.data['authors'] == [new_author.pk]
        assert response.data['category'] == new_category.name

    def test_patch_book_unauthenticated(self):
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.patch(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_book_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.patch(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_book_super_user(self):
        self.client.force_authenticate(self.super_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.patch(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'NewTitleBookTest'
        assert response.data['authors'] == [new_author.pk]
        assert response.data['category'] == new_category.name

    def test_patch_book_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        book = BookFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        new_author = AuthorFactory()
        new_category = CategoryFactory()
        response = self.client.patch(
            url,
            {
                'title': 'NewTitleBookTest',
                'authors': [str(new_author.pk)],
                'category': new_category.name,
            },
        )
        assert response.status_code == HTTP_200_OK
        assert response.data['title'] == 'NewTitleBookTest'
        assert response.data['authors'] == [new_author.pk]
        assert response.data['category'] == new_category.name

    def test_delete_book_unauthenticated(self):
        book = CategoryFactory()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_book_authenticated_common_user(self):
        book = CategoryFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_book_authenticated_admin_user(self):
        book = BookFactory()
        self.client.force_authenticate(self.admin_user)
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Book.objects.filter(pk=book.pk).exists()

    def test_delete_book_authenticated_super_user(self):
        book = BookFactory()
        self.client.force_authenticate(self.super_user)
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Book.objects.filter(pk=book.pk).exists()
