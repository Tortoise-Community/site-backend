import json
import socket
import logging

import httpx

from django.conf import settings
from django.core.mail import send_mail


logger = logging.getLogger("Generic Logger")
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(message)s')
fileHandler = logging.FileHandler(filename="error.log")
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)


class WebhookHandler:

    headers = {'Content-Type': 'application/json'}
    resp = None

    def __init__(self, webhook_id, secret):
        self.webhook_id = webhook_id
        self.secret = secret
        self.url = "https://discordapp.com/api/webhooks/{}/{}".format(self.webhook_id, self.secret)

    def _send_to_webhook(self, payload):
        try:
            self.resp = httpx.post(url=self.url, headers=self.headers, json=payload)
        except Exception as exp:
            log_error(exp, payload)

    def send_embed(self, payload: dict):
        payload = {"embeds": [payload]}
        self._send_to_webhook(payload)

    def send_message(self, message: str):
        payload = {"content": message}
        self._send_to_webhook(payload)


alert_hook = WebhookHandler(settings.WEBHOOK_ID, settings.WEBHOOK_SECRET)



class EmailHandler:

    @staticmethod
    def send_email(recipient, subject, message):
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email='tortoise Community <tortoisecommunity@gmail.com>',
                recipient_list=['{}'.format(recipient)]
            )
        except Exception as exp:
            embed = {
                "title": "Exception while sending email",
                "description": (
                    f"Exception: {exp}\n\n"
                    f"Recipient: {recipient}"
                    f"Subject: {subject}"
                ),
                "color": 0xff0000
            }
            alert_hook.send_embed(embed)


def log_error(exp, msg):
    logger.debug(f"{exp} raised on activity {msg}")
    embed = {
        "title": "API Error",
        "description": f"`{exp}`\n\n",
        "color": 0xff0000
    }
    alert_hook.send_embed(embed)
