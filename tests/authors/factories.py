import factory

from authors.models import Author


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.faker.Faker('name')
