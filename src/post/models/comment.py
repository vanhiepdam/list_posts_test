from django.db import models

from shared.models.base_model import BaseModel


class Comment(BaseModel):
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    posted_by = models.ForeignKey(
        "user_profile.User",
        on_delete=models.PROTECT,
        related_name="post_comments",
    )

    def __str__(self) -> str:
        return self.preview

    @property
    def preview(self) -> str:
        return self.content[:20] + "..." if len(self.content) > 20 else self.content
