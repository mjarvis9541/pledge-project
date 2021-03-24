from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass
    # Any additional fields depending on future requirements

    def __str__(self):
        return self.username
