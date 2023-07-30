# type: ignore
import pytest

from post.tests.factories.comment import CommentFactory

pytestmark = [pytest.mark.django_db]


class TestCommentModel:
    def test_preview__content_length_less_than_20(self):
        # Arrange
        comment = CommentFactory(content="comment 1")

        # Assert
        assert comment.preview == "comment 1"

    def test_preview__content_length_more_than_20(self):
        # Arrange
        comment = CommentFactory(content="comment 1" * 10)

        # Assert
        assert comment.preview == comment.content[:20] + "..."
