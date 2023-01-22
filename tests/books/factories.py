import random

import factory

from books.models import Book
from tests.authors.factories import AuthorFactory
from tests.categories.factories import CategoryFactory


def factory_get_authors():
    num_of_authors = random.randint(1, 3)
    authors = AuthorFactory.create_batch(num_of_authors)

    return authors


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.faker.Faker('catch_phrase')
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create or extracted:
            return

        authors = factory_get_authors()
        self.authors.add(*authors)
