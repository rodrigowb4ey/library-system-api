from uuid import uuid4

from django.db import models

from authors.models import Author


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers', null=True, blank=True)
    authors = models.ManyToManyField(Author)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f'{self.title}'
