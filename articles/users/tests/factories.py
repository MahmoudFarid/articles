import factory

from factory.django import DjangoModelFactory as Factory
from django.contrib.auth import get_user_model


class UserFactory(Factory):
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    name = factory.Faker('name')
    is_active = True

    class Meta:
        model = get_user_model()
