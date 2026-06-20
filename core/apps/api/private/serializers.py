from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator

from ..models import User, Guild, Member


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("email",)
        extra_kwargs = {
            'id': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class GuildDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        fields = "__all__"
        extra_kwargs = {
            'id': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class GuildMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guild
        exclude = ("id", "name")


class MemberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        exclude = ("user", "guild")


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("name", "email", "tag", "id")
