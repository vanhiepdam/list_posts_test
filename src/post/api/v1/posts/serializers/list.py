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
    most_recent_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", "author", "most_recent_comment"]

    def get_most_recent_comment(self, obj: Post) -> str | None:
        if not hasattr(obj, "most_recent_comment") or not obj.most_recent_comment:
            return None

        comment_words = obj.most_recent_comment.split(" ")
        if len(comment_words) > 8:
            comment_words = comment_words[:8]
            comment_words.append("...")
        return " ".join(comment_words)
