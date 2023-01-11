from uuid import uuid4

from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid4)

    def __str__(self):
        return f'{self.name}'
