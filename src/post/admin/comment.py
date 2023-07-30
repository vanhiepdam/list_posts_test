from django.contrib import admin

from post.models import Comment
from shared.django_admins.base_admin import BaseModelAdmin


@admin.register(Comment)
class CommentAdmin(BaseModelAdmin):
    list_display = [
        "id",
        "post",
        "content",
    ]
    autocomplete_fields = [
        "post",
        "posted_by",
    ]
