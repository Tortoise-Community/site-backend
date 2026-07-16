from django.db import models
from django.contrib.auth.models import AbstractUser

from core.utils.misc import DiscordIDField


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    discord_id = DiscordIDField(unique=True)
    display_name = models.CharField(max_length=32)
    _avatar = models.CharField(max_length=32, blank=True, null=True)
    verified = models.BooleanField(default=False)

    @property
    def avatar(self):
        if self._avatar is not None:
            return f"https://cdn.discordapp.com/avatars/{self.id}/{self._avatar}.png"
        return "https://cdn.discordapp.com/embed/avatars/4.png"

    def get_decrypted_token(self, service, token_type):
        return self.oauth_tokens.filter(service=service, token_type=token_type).first()


class OauthToken(models.Model):
    TOKEN_TYPES = (
        ("access", "Access Token"),
        ("refresh", "Refresh Token"),
    )
    SERVICE_TYPES = (
        ("discord", "Discord Token"),
        ("github", "Github Token"),
        ("google", "Google Token"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="oauth_tokens")
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=7, choices=TOKEN_TYPES, default="access")
    service = models.CharField(max_length=7, choices=SERVICE_TYPES, default="discord")
    value = models.CharField(max_length=100, null=True, blank=True)
    nonce = models.BinaryField()
    expiry = models.DateTimeField(null=True, blank=True)



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

class BannedMember(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    expires = models.DateTimeField(null=True, blank=True)
