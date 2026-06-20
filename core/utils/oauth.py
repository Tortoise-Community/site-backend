import httpx
from django.conf import settings


class Oauth(object):
    client_id = settings.OAUTH_CLIENT_ID
    client_secret = settings.OAUTH_CLIENT_SECRET
    scope = "identify%20email"
    redirect_uri = "http://dashboard.localhost.co:8000/login/"
    discord_login_url = "https://discord.com/api/oauth2/authorize?client_id={}&" \
                        "redirect_uri={}&response_type=code&scope={}".format(client_id, redirect_uri, scope)
    discord_token_url = "https://discord.com/api/oauth2/token"
    discord_api_url = "https://discord.com/api"
    client_id = settings.OAUTH_CLIENT_ID

    def __init__(self,
                 redirect_uri="http://dashboard.localhost.co:8000/login/",
                 scope="identify%20email"
                 ):
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.discord_login_url = (
            f"https://discord.com/api/oauth2/authorize?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}&response_type=code&scope={self.scope}"
        )

    def get_token_json(self, code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'scope': self.scope
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        tokens = httpx.post(url=self.discord_token_url, data=payload, headers=headers)
        return tokens.json()

    @staticmethod
    def get(access_token, endpoint):

        headers = {"Authorization": f"Bearer {access_token}"}
        response_object = httpx.get(url=endpoint, headers=headers)
        return response_object.json()

    def get_user_json(self, access_token):
        url = f"{self.discord_api_url}/users/@me"
        return self.get(access_token, endpoint=url)

    def get_guild_info_json(self, access_token):
        url = f"{self.discord_api_url}/users/@me/guilds"
        return self.get(access_token, endpoint=url)
