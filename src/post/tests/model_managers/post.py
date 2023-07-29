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

    def test_full_prefetch(self, post_data):
        # Arrange
        CommentFactory.create_batch(2, post=post_data["active_post_1"])

        # Act
        active_posts = Post.objects.all()

        # Assert
        assert active_posts.count() == 2
        assert post_data["active_post_1"] in active_posts
        assert post_data["active_post_2"] in active_posts
