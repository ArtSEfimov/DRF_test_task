from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_phone',
                                related_query_name='user_phone_query'
                                )
    phone = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, unique=True)

