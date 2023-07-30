from rest_framework import serializers

from post.models import Post
from shared.viewsets.serializers import BaseModelSerializer
from user_profile.models import User


class ListPostSerializerAuthorV1(BaseModelSerializer):
    nickname = serializers.CharField(source="get_nickname")

    class Meta:
        model = User
        fields = ["id", "username", "nickname"]


class ListPostSerializerV1(BaseModelSerializer):
    author = ListPostSerializerAuthorV1()
    most_recent_comment = serializers.CharField()

    class Meta:
        model = Post
        fields = ["id", "title", "author", "most_recent_comment"]
