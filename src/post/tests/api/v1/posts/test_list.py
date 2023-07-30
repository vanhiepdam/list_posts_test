# type: ignore
import pytest

from post.tests.factories.comment import CommentFactory
from post.tests.factories.post import PostFactory
from user_profile.tests.factories.user import UserFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def post_data():
    post_1 = PostFactory(
        author=UserFactory(nickname="TOSHIBA"),
    )
    post_2 = PostFactory()
    post_3 = PostFactory()
    comment_1 = CommentFactory(content="comment 1", post=post_3)
    comment_2 = CommentFactory(content="comment 2", post=post_3)
    comment_3 = CommentFactory(content="comment 3", post=post_2)
    comment_4 = CommentFactory(content="comment 4", post=post_2)
    comment_5 = CommentFactory(content="comment 5", post=post_2)

    return {
        "post_1": post_1,
        "post_2": post_2,
        "post_3": post_3,
        "comment_1": comment_1,
        "comment_2": comment_2,
        "comment_3": comment_3,
        "comment_4": comment_4,
        "comment_5": comment_5,
    }


class TestListPostApiV1:
    def test_success__list_all__no_query_params(self, post_data, api_client):
        # Arrange
        url = "/api/v1/posts"

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200
        assert len(response.data["results"]) == 3
        assert response.data["results"][0]["id"] == post_data["post_3"].id
        assert response.data["results"][0]["title"] == post_data["post_3"].title
        assert response.data["results"][0]["author"] == {
            "id": post_data["post_3"].author.id,
            "username": post_data["post_3"].author.username,
            "nickname": post_data["post_3"].author.get_nickname(),
        }
        assert response.data["results"][0]["most_recent_comment"] == post_data["comment_2"].content

        assert response.data["results"][1]["id"] == post_data["post_2"].id
        assert response.data["results"][1]["title"] == post_data["post_2"].title
        assert response.data["results"][1]["author"] == {
            "id": post_data["post_2"].author.id,
            "username": post_data["post_2"].author.username,
            "nickname": post_data["post_2"].author.get_nickname(),
        }
        assert response.data["results"][1]["most_recent_comment"] == post_data["comment_5"].content

        assert response.data["results"][2]["id"] == post_data["post_1"].id
        assert response.data["results"][2]["title"] == post_data["post_1"].title
        assert response.data["results"][2]["author"] == {
            "id": post_data["post_1"].author.id,
            "username": post_data["post_1"].author.username,
            "nickname": post_data["post_1"].author.get_nickname(),
        }
        assert response.data["results"][2]["most_recent_comment"] is None

    def test_success__list_all__custom_items_in_page_query_params(self, post_data, api_client):
        # Arrange
        url = "/api/v1/posts?page_size=1"

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == post_data["post_3"].id
        assert response.data["results"][0]["title"] == post_data["post_3"].title
        assert response.data["results"][0]["author"] == {
            "id": post_data["post_3"].author.id,
            "username": post_data["post_3"].author.username,
            "nickname": post_data["post_3"].author.get_nickname(),
        }
        assert response.data["results"][0]["most_recent_comment"] == post_data["comment_2"].content
        assert "api/v1/posts?page=2&page_size=1" in response.data["next"]

    def test_success__list_all__long_comment(self, post_data, api_client):
        # Arrange
        url = "/api/v1/posts?page_size=1"
        CommentFactory(
            content="Lorem ipsum dolor sit amet, consectetur adipiscing elit sollicitudin id",
            post=post_data["post_3"],
        )

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["id"] == post_data["post_3"].id
        assert response.data["results"][0]["title"] == post_data["post_3"].title
        assert response.data["results"][0]["author"] == {
            "id": post_data["post_3"].author.id,
            "username": post_data["post_3"].author.username,
            "nickname": post_data["post_3"].author.get_nickname(),
        }
        assert (
            response.data["results"][0]["most_recent_comment"]
            == "Lorem ipsum dolor sit amet, consectetur adipiscing elit ..."
        )
        assert "api/v1/posts?page=2&page_size=1" in response.data["next"]
