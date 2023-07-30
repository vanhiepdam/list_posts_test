from django.db.models.signals import post_save

import factory
from factory.django import DjangoModelFactory

from post.models import Comment
from post.tests.factories.post import PostFactory
from user_profile.tests.factories.user import UserFactory


@factory.django.mute_signals(post_save)
class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    content = factory.Faker("sentence")
    posted_by = factory.SubFactory(UserFactory)
