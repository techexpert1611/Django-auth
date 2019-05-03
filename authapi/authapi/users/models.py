from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(name="phone", max_length=10, null=True)
    photo = models.ImageField(name="photo", upload_to='photos/', null=True)

