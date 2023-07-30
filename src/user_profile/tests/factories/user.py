from django.db.models.signals import post_save

import factory
from factory.django import DjangoModelFactory

from user_profile.models import User


@factory.django.mute_signals(post_save)
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
