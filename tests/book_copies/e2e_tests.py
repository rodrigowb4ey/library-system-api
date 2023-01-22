import base64
import tempfile
from contextlib import contextmanager
from datetime import date

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from books.models import BookCopy

from ..books.factories import BookFactory
from ..publishers.factories import PublisherFactory
from .factories import BookCopyFactory


@pytest.mark.django_db
class TestBookCopyEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('bookcopy-list')
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

    @classmethod
    @contextmanager
    def _generate_random_image_file(self):
        with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp_file:
            image = Image.new('RGB', size=(1024, 768))
            image.save(tmp_file, format='jpeg')
            tmp_file.seek(0)

            yield tmp_file

    @classmethod
    def _generate_random_image_in_base64(self):
        with self._generate_random_image_file() as image_file:
            encoded_string = base64.b64encode(image_file.read())

        return encoded_string.decode('utf-8')

    def test_get_book_copies_unauthenticated(self):
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_book_copies_authenticated(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_book_copy_by_id_unauthenticated(self):
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.get(url)
        data = response.json()
        cover_path = data['cover'].split('http://testserver')[-1]

        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(book_copy.pk)
        assert data['date_published'] == book_copy.date_published
        assert data['book'] == str(book_copy.book.pk)
        assert data['publisher'] == book_copy.publisher.name
        assert cover_path == book_copy.cover.path

    def test_get_book_copy_by_id_authenticated(self):
        self.client.force_authenticate(self.common_user)
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.get(url)
        data = response.json()
        cover_path = data['cover'].split('http://testserver')[-1]

        assert response.status_code == HTTP_200_OK
        assert data['id'] == str(book_copy.pk)
        assert data['date_published'] == book_copy.date_published
        assert data['book'] == str(book_copy.book.pk)
        assert data['publisher'] == book_copy.publisher.name
        assert cover_path == book_copy.cover.path

    def test_post_book_copy_unauthenticated(self):
        with self._generate_random_image_file() as image_file:
            book = BookFactory()
            date_published = date.today()
            publisher = PublisherFactory()
            response = self.client.post(
                self.url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_book_copy_authenticated_common_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.common_user)
            book = BookFactory()
            date_published = date.today()
            publisher = PublisherFactory()
            response = self.client.post(
                self.url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_book_copy_authenticated_admin_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.admin_user)
            book = BookFactory()
            date_published = date.today()
            publisher = PublisherFactory()
            response = self.client.post(
                self.url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_201_CREATED
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_post_book_copy_authenticated_super_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.super_user)
            book = BookFactory()
            date_published = date.today()
            publisher = PublisherFactory()
            response = self.client.post(
                self.url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_201_CREATED
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_post_book_copy_with_cover_image_in_b64(self):
        self.client.force_authenticate(self.admin_user)
        book = BookFactory()
        date_published = date.today()
        publisher = PublisherFactory()
        cover_b64 = self._generate_random_image_in_base64()
        response = self.client.post(
            self.url,
            {
                'book': str(book.pk),
                'date_published': date_published,
                'publisher': publisher.name,
                'cover': cover_b64,
            },
        )
        assert response.status_code == HTTP_201_CREATED
        assert response.data['date_published'] == date_published.isoformat()
        assert response.data['book'] == book.pk
        assert response.data['publisher'] == publisher.name

    def test_put_book_copy_unauthenticated(self):
        with self._generate_random_image_file() as image_file:
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.put(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_book_copy_authenticated_common_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.common_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.put(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_book_copy_super_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.super_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.put(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_200_OK
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_put_book_copy_authenticated_admin_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.admin_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.put(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_200_OK
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_patch_book_copy_unauthenticated(self):
        with self._generate_random_image_file() as image_file:
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.patch(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_book_copy_authenticated_common_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.common_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.patch(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_book_copy_super_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.super_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.patch(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_200_OK
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_patch_book_copy_authenticated_admin_user(self):
        with self._generate_random_image_file() as image_file:
            self.client.force_authenticate(self.admin_user)
            book_copy = BookCopyFactory()
            url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
            date_published = date.today()
            book = BookFactory()
            publisher = PublisherFactory()
            response = self.client.patch(
                url,
                {
                    'book': str(book.pk),
                    'date_published': date_published,
                    'publisher': publisher.name,
                    'cover': image_file,
                },
            )
            assert response.status_code == HTTP_200_OK
            assert (
                response.data['date_published'] == date_published.isoformat()
            )
            assert response.data['book'] == book.pk
            assert response.data['publisher'] == publisher.name

    def test_delete_book_copy_unauthenticated(self):
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_book_copy_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_book_copy_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not BookCopy.objects.filter(pk=book_copy.pk).exists()

    def test_delete_book_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        book_copy = BookCopyFactory()
        url = reverse('bookcopy-detail', kwargs={'pk': book_copy.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not BookCopy.objects.filter(pk=book_copy.pk).exists()
