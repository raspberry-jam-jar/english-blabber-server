import factory

from class_room import models


class SocialUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.SocialUser

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('first_name')
    date_of_birth = factory.Faker('date')
