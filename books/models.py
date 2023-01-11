from uuid import uuid4

from django.db import models


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers', null=True, blank=True)

    def __str__(self):
        return f'{self.title}'
