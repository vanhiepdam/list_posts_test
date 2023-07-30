from django.db.models import QuerySet

from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from post.api.v1.posts.serializers.list import ListPostSerializerV1
from post.models import Post


class PostViewSetV1(GenericViewSet, ListModelMixin):
    serializer_class = ListPostSerializerV1
    permission_classes = [AllowAny]

    def get_queryset(self) -> QuerySet[Post]:
        return (
            Post.objects.all().select_related("author").with_most_recent_comment().order_by("-id")
        )
