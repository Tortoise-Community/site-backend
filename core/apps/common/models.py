from django.db import models
from django.contrib.auth.models import AbstractUser

from core.utils.misc import DiscordIDField


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    discord_id = DiscordIDField(unique=True)
    display_name = models.CharField(max_length=32)
    _avatar = models.CharField(max_length=32, blank=True, null=True)
    verified = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    discord_access_token = models.CharField(max_length=100, null=True, blank=True)
    discord_refresh_token = models.CharField(max_length=100, null=True, blank=True)
    discord_access_token_expiry = models.DateTimeField(null=True, blank=True)

    @property
    def avatar(self):
        if self._avatar is not None:
            return f"https://cdn.discordapp.com/avatars/{self.id}/{self._avatar}.png"
        return "https://cdn.discordapp.com/embed/avatars/4.png"

class Guild(models.Model):
    id = DiscordIDField(primary_key=True)
    name = models.CharField(max_length=100)

class Member(models.Model):
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    guild: Guild = models.ForeignKey(Guild, on_delete=models.CASCADE, related_name="members")
    join_date = models.DateTimeField(auto_now_add=True)
    leave_date = models.DateTimeField(null=True, blank=True, default=None)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="invitees", null=True, blank=True)


    class Meta:
        unique_together = (('user', 'guild'), ('user', 'guild', 'invited_by'))
