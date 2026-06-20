from django.db import models
from django.contrib.auth.models import AbstractUser

from core.utils.misc import DiscordIDField


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    discord_id = DiscordIDField(primary_key=True)
    display_name = models.CharField(max_length=32)
    avatar = models.URLField(max_length=150, blank=True, null=True)
    verified = models.BooleanField(default=False)

class Guild(models.Model):
    id = DiscordIDField(primary_key=True)
    name = models.CharField(max_length=100)


class Member(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    guild: Guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name="members")
    join_date = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateTimeField(null=True, blank=True, default=None)
    invited_by = models.ForeignKey("Invite", on_delete=models.SET_NULL, related_name="members", null=True, blank=True)

    class Meta:
        unique_together = (('user', 'guild'), ('user', 'guild', 'invited_by'))
