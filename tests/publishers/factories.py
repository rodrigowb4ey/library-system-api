import factory

from books.models import Publisher


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.faker.Faker('company')
