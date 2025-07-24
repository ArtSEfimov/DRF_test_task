from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='user_profile',
                                related_query_name='user_profile_query'
                                )
    phone = models.CharField(max_length=20, unique=True)
    own_invite_code = models.CharField(max_length=6, unique=True)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, related_name='invited_users',
                                   null=True, blank=True)
