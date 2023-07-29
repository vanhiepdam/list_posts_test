from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=255, null=True, blank=True)

    def get_nickname(self) -> str:
        return self.nickname or self.username
