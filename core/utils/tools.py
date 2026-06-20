from django.conf import settings
from django.db.models.signals import post_save, post_delete

from core.apps.api.models import Rule
from .handlers import SocketHandler, WebhookHandler


webhook = WebhookHandler(settings.WEBHOOK_ID, settings.WEBHOOK_SECRET)
bot_socket = SocketHandler(
    settings.BOT_SOCKET_IP,
    int(settings.BOT_SOCKET_PORT),
    settings.BOT_SOCKET_TOKEN
)


def reload_rules(_sender, **_kwargs):
    bot_socket.signal("rules")


def reload_server_utils(_sender, **_kwargs):
    bot_socket.signal("server_meta")
