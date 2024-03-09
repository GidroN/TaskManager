from django.db import models
from django.contrib.auth.models import User


class CustomUser(User):
    class Meta:
        unique_together = ('username', 'email')
