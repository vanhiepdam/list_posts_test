# type: ignore
import pytest

from post.models import Post
from post.tests.factories.comment import CommentFactory
from post.tests.factories.post import PostFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def post_data():
    active_post_1 = PostFactory()
    active_post_2 = PostFactory()
    inactive_post_1 = PostFactory(is_active=False)
    inactive_post_2 = PostFactory(is_active=False)

    return {
        "active_post_1": active_post_1,
        "active_post_2": active_post_2,
        "inactive_post_1": inactive_post_1,
        "inactive_post_2": inactive_post_2,
    }


class TestPostManager:
    def test_active_post_manager_queryset(self, post_data):
        # Act
        active_posts = Post.objects.all()

        # Assert
        assert active_posts.count() == 2
        assert post_data["active_post_1"] in active_posts
        assert post_data["active_post_2"] in active_posts

    def test_all_post_manager_queryset(self, post_data):
        # Act
        active_posts = Post.all_objects.all()

        # Assert
        assert active_posts.count() == 4
        assert post_data["active_post_1"] in active_posts
        assert post_data["active_post_2"] in active_posts
        assert post_data["inactive_post_1"] in active_posts
        assert post_data["inactive_post_2"] in active_posts

    def test_with_most_recent_comments__have_comments(self, post_data):
        # Arrange
        post = post_data["active_post_1"]
        CommentFactory(post=post, content="comment 1")
        CommentFactory(post=post, content="comment 2")

        # Act
        post = Post.objects.all().with_most_recent_comment().get(id=post.id)

        # Assert
        assert post.most_recent_comment == "comment 2"

    def test_with_most_recent_comments__have_no_comments(self, post_data):
        # Arrange
        post = post_data["active_post_1"]

        # Act
        post = Post.objects.all().with_most_recent_comment().get(id=post.id)

        # Assert
        assert post.most_recent_comment is None
