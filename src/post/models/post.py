from django.db import models

from post.model_managers.post import (
    ActivePostManager,
    AllPostManager,
)
from shared.models.base_model import BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, db_index=True)
    author = models.ForeignKey("user_profile.User", on_delete=models.PROTECT, related_name="posts")

    objects = ActivePostManager()
    all_objects = AllPostManager()

    def __str__(self) -> str:
        title: str = self.title
        return title
