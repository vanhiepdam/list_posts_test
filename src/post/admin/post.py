from django.contrib import admin

from post.models import Post
from shared.django_admins.base_admin import BaseModelAdmin


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    list_display = [
        "id",
        "title",
        "created_at",
    ]
    autocomplete_fields = [
        "author",
    ]
    search_fields = [
        "title",
    ]
