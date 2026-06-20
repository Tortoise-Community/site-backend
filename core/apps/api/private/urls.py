from rest_framework import routers
from django.urls import path, include

from .views import (
    UserDataView, SuggestionDataView, MemberDataView, GuildDataView,
    RulesDataView, RolesDataView, InfractionDataView,
    MemberWarningView, StrikeDataView
)


router = routers.DefaultRouter()


urlpatterns = [
    path('guild/', GuildDataView.as_view()),
    path('guild/<int:guild_id>/', GuildDataView.as_view()),

    path('members/', MemberDataView.as_view()),
    path('members/<int:guild_id>/', MemberDataView.as_view()),
    path('members/<int:guild_id>/<int:user_id>/', MemberDataView.as_view()),

    path('user/<int:user_id>/', UserDataView.as_view()),
    path('user/', UserDataView.as_view()),
    path('user/<int:user_id>/strikes/', StrikeDataView.as_view()),

    path('strikes/', StrikeDataView.as_view()),

    path('warnings/', MemberWarningView.as_view()),
    path('warnings/<int:guild_id>/<int:user_id>/', MemberWarningView.as_view()),
    path('warnings/<int:guild_id>/', MemberWarningView.as_view()),

    path('infractions/', InfractionDataView.as_view()),
    path('infractions/<int:guild_id>/', InfractionDataView.as_view()),
    path('infractions/<int:guild_id>/<int:user_id>/', InfractionDataView.as_view()),
]
