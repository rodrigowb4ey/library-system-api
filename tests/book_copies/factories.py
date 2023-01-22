from uuid import uuid4

import factory
from django.core.files.base import ContentFile

from books.models import BookCopy

from ..books.factories import BookFactory
from ..publishers.factories import PublisherFactory


class BookCopyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookCopy

    date_published = factory.faker.Faker('date')
    book = factory.SubFactory(BookFactory)
    publisher = factory.SubFactory(PublisherFactory)
    cover = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ),
            f'{uuid4()}.jpg',
        )
    )
