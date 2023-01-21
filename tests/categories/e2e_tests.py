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

from books.models import Category

from .factories import CategoryFactory


@pytest.mark.django_db
class TestCategoryEndpoint:
    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('category-list')
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

    def test_get_categories_unauthenticated(self):
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_categories_authenticated(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.get(self.url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert (
            len(data['results']) == 0
        )  # Assumes initial state is an empty list

    def test_get_category_by_id_unauthenticated(self):
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == int(category.pk)
        assert data['name'] == category.name

    def test_get_category_by_id_authenticated(self):
        self.client.force_authenticate(self.common_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.get(url)
        data = response.json()
        assert response.status_code == HTTP_200_OK
        assert data['id'] == int(category.pk)
        assert data['name'] == category.name

    def test_post_category_unauthenticated(self):
        response = self.client.post(self.url, {'name': 'ExampleCategory'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_category_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        response = self.client.post(self.url, {'name': 'ExampleCategory'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_post_category_authenticated_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(self.url, {'name': 'ExampleCategory'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'ExampleCategory'

    def test_post_category_authenticated_super_user(self):
        self.client.force_authenticate(self.super_user)
        response = self.client.post(self.url, {'name': 'ExampleCategory'})
        assert response.status_code == HTTP_201_CREATED
        assert response.data['name'] == 'ExampleCategory'

    def test_put_category_unauthenticated(self):
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.put(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_category_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.put(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_put_category_super_user(self):
        self.client.force_authenticate(self.super_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.put(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewCategoryName'

    def test_put_category_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.put(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewCategoryName'

    def test_patch_category_unauthenticated(self):
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.patch(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_category_authenticated_common_user(self):
        self.client.force_authenticate(self.common_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.patch(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_patch_category_super_user(self):
        self.client.force_authenticate(self.super_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.patch(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewCategoryName'

    def test_patch_category_admin_user(self):
        self.client.force_authenticate(self.admin_user)
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.patch(url, {'name': 'NewCategoryName'})
        assert response.status_code == HTTP_200_OK
        assert response.data['name'] == 'NewCategoryName'

    def test_delete_category_unauthenticated(self):
        category = CategoryFactory()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_category_authenticated_common_user(self):
        category = CategoryFactory()
        self.client.force_authenticate(self.common_user)
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_category_authenticated_admin_user(self):
        category = CategoryFactory()
        self.client.force_authenticate(self.admin_user)
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=category.pk).exists()

    def test_delete_category_authenticated_super_user(self):
        category = CategoryFactory()
        self.client.force_authenticate(self.super_user)
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT
        assert not Category.objects.filter(pk=category.pk).exists()
