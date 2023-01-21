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

from books.models import Publisher

from .factories import PublisherFactory


@pytest.mark.django_db
class TestPublisherEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('publisher-list')
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

    def test_get_publishers_unauthenticated(self):
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_publishers_authenticated(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_publisher_by_id_unauthenticated(self):
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == int(publisher.pk)
        assert data['name'] == publisher.name

    def test_get_publisher_by_id_authenticated(self):
        self.client.force_authenticate(self.common_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == int(publisher.pk)
        assert data['name'] == publisher.name

    def test_post_publisher_unauthenticated(self):
        response = self.client.post(self.url, {'name': 'Examplepublisher'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_publisher_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.post(self.url, {'name': 'Examplepublisher'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_publisher_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(self.url, {'name': 'Examplepublisher'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'Examplepublisher'

    def test_post_publisher_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        response = self.client.post(self.url, {'name': 'Examplepublisher'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'Examplepublisher'

    def test_put_publisher_unauthenticated(self):
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.put(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_publisher_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.put(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_publisher_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.put(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewPublisherName'

    def test_put_publisher_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.put(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewPublisherName'

    def test_patch_publisher_unauthenticated(self):
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.patch(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_publisher_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.patch(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_publisher_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.patch(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewPublisherName'

    def test_patch_publisher_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.patch(url, {'name': 'NewPublisherName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewPublisherName'

    def test_delete_publisher_unauthenticated(self):
        publisher = PublisherFactory()
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_publisher_authenticated_common_user(self):
        publisher = PublisherFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_publisher_authenticated_admin_user(self):
        publisher = PublisherFactory()
        self.client.force_authenticate(self.admin_user)
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Publisher.objects.filter(pk=publisher.pk).exists()

    def test_delete_publisher_authenticated_super_user(self):
        publisher = PublisherFactory()
        self.client.force_authenticate(self.super_user)
        url = reverse('publisher-detail', kwargs={'pk': publisher.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Publisher.objects.filter(pk=publisher.pk).exists()
