from datetime import datetime, timezone, timedelta

from rest_framework.views import APIView

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from core.utils.oauth import Oauth
from core.utils.hash import Hashing
from core.apps.common.models import User
from .serializers import CookieTokenRefreshSerializer


oauth = Oauth(scope="email%20identify")
hasher = Hashing()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.display_name
    refresh['avatar'] = user.avatar
    refresh['banned'] = user.banned

    return {
               'access': str(refresh.access_token),
           }, str(refresh)

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        return super().finalize_response(request, response, *args, **kwargs)

class LoginView(APIView):
    model = User
    permission_classes = AllowAny,

    # def get(self, request):
    #     return Response({"url": oauth.discord_login_url})

    def get(self, request):
        code = request.data.get("code")
        if code:
            token_json = oauth.get_token_json(code)
            user_json = oauth.get_user_json(token_json.get("access_token"))
            email = user_json.get("email")
            try:
                user = self.model.objects.get(email=email)
                access_token_response, refresh_token = get_tokens_for_user(user)
                response = Response(access_token_response, status=status.HTTP_200_OK)
                response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 3, httponly=True)
                return response
            except self.model.DoesNotExist:
                if user_json.get("verified"):
                    user = self.model.objects.create_user(
                        email=user_json.get("email"),
                        username=user_json.get("email"),
                        password=hasher.hashed_user_pass(user_json.get("email"), user_json.get("id")),
                        _avatar = user_json.get("avatar"),
                        discord_id=user_json.get("id"),
                        display_name=user_json.get("username")[:32],
                        discord_access_token=token_json.get("access_token"),
                        discord_refresh_token=token_json.get("refresh_token"),
                        discord_access_token_expiry=
                        datetime.now(timezone.utc) + timedelta(seconds=token_json.get("expires_in") - 25)
                    )
                    access_token_response, refresh_token = get_tokens_for_user(user)
                    response = Response(access_token_response, status=status.HTTP_201_CREATED)
                    response.set_cookie('refresh_token', refresh_token, max_age=3600 * 24 * 3, httponly=True)
                    return response
                else:
                    return Response(
                        {"message": "Discord email verification pending"},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )
        return Response({"message": "No code received"}, status=status.HTTP_400_BAD_REQUEST)
