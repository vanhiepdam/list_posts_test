# type: ignore
import pytest

from user_profile.tests.factories.user import UserFactory


pytestmark = [pytest.mark.django_db]


class TestUserModel:
    def test_get_nickname__no_nickname(self):
        # Arrange
        user = UserFactory()

        # Act
        nickname = user.get_nickname()

        # Assert
        assert nickname == user.username

    def test_get_nickname__has_nickname(self):
        # Arrange
        user = UserFactory(nickname="TOSHIBA")

        # Act
        nickname = user.get_nickname()

        # Assert
        assert nickname == "TOSHIBA"
