from django.db.models.signals import post_save

import factory
from factory.django import DjangoModelFactory

from post.models import Post
from user_profile.tests.factories.user import UserFactory


@factory.django.mute_signals(post_save)
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=5)
