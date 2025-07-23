from django.contrib.auth.models import User
from django.db import models


class UserPhone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True)
