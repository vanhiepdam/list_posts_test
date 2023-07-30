from django.db import models
from django.db.models import QuerySet

from shared.models.base_manager import BaseManager


class PostQuerySet(QuerySet):
    def with_most_recent_comment(self) -> QuerySet:
        from post.models import Comment

        comment_subquery = Comment.objects.filter(
            post=models.OuterRef("id")
        ).order_by("-id").values("content")[:1]
        return self.annotate(
            most_recent_comment=models.Subquery(comment_subquery),
        )


class ActivePostManager(BaseManager):
    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db).filter(is_active=True)


class AllPostManager(BaseManager):
    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db)
