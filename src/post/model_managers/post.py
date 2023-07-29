from django.contrib.auth.models import UserManager as BuiltinUserManager
from django.db.models import QuerySet


class PostQuerySet(QuerySet):
    def full_prefetch(self) -> QuerySet:
        return self.select_related("author").prefetch_related(
            "comments",
        )


class ActivePostManager(BuiltinUserManager):
    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db).filter(
            is_active=True
        )


class AllPostManager(BuiltinUserManager):
    def get_queryset(self) -> QuerySet:
        return PostQuerySet(self.model, using=self._db)
