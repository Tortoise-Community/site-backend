from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.utils.handlers import log_error
from core.utils.mixins import ResponseMixin
from ..models import Member, Guild, User
from .serializers import (
    MemberDataSerializer, GuildDataSerializer, GuildMetaSerializer, UserDataSerializer,
)


class MemberDataView(APIView, ResponseMixin):
    model = Member
    serializers = MemberDataSerializer

    def get(self, request, user_id=None, guild_id=None):
        if guild_id and user_id is not None:
            queryset = get_object_or_404(self.model, user__id=user_id, guild__id=guild_id)
            serializer = self.serializers(queryset)
            return Response(serializer.data, status=200)
        elif guild_id is not None:
            queryset = self.model.objects.filter(guild__id=guild_id)
            serializer = self.serializers(queryset, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)
        else:
            queryset = self.model.objects.all()
            serializer = self.serializers(queryset, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, guild_id=None, user_id=None):
        if guild_id or user_id is not None:
            return self.json_response_405()
        else:
            try:
                user, created = User.objects.get_or_create(**request.data.pop("user"))
                guild = Guild.objects.get(id=request.data.get("guild_id"))
                Member.objects.create(user=user, guild=guild)
            except Exception as e:
                log_error(Exception, e)
                return self.json_response_500()
            return Response(status=201)

    def put(self, request, user_id=None, guild_id=None):
        if user_id and guild_id is not None:
            queryset = get_object_or_404(self.model, user__id=user_id, guild__id=guild_id)
            serializer = self.serializers(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return self.json_response_500()
        else:
            return self.json_response_405()

    def delete(self, request, user_id=None, guild_id=None):
        if user_id and guild_id is not None:
            queryset = get_object_or_404(self.model, user__id=user_id, guild__id=guild_id)
            queryset.delete()
            return self.json_response_204()
        else:
            return self.json_response_405()



class GuildDataView(APIView, ResponseMixin):
    model = Guild
    serializers = GuildDataSerializer

    def get(self, request, guild_id=None):
        if guild_id is not None:
            queryset = get_object_or_404(self.model, id=guild_id)
            serializer = self.serializers(queryset)
            return Response(serializer.data, status=200)
        else:
            queryset = self.model.objects.all()
            serializer = self.serializers(queryset, many=True)
            return Response(serializer.data, status=200)

    def post(self, request, guild_id=None):
        if guild_id is not None:
            return self.json_response_405()
        else:
            serializer = self.serializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return self.json_response_400()

    def put(self, request, guild_id=None):
        if guild_id is None:
            return self.json_response_405()
        queryset = get_object_or_404(self.model, id=guild_id)
        serializer = GuildMetaSerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return self.json_response_500()


class UserDataView(APIView, ResponseMixin):
    model = User
    serializers = UserDataSerializer

    def get(self, request, user_id=None):
        if user_id is not None:
            queryset = get_object_or_404(self.model, id=user_id)
            serializer = self.serializers(queryset)
            return Response(serializer.data, status=200)
        else:
            limit = self.request.query_params.get("limit", None)
            verified = self.request.query_params.get("verified", None)
            perks_lt = self.request.query_params.get("perks_lt", None)
            perks_gt = self.request.query_params.get("perks_gt", None)
            query_filter = {}
            if verified:
                query_filter["verified"] = verified
            if perks_lt:
                query_filter["perks__lt"] = perks_lt
            if perks_gt:
                query_filter["perks__gt"] = perks_gt
            queryset = self.model.objects.filter(**query_filter)[:int(limit) if limit else None]
            serializer = self.serializers(queryset, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, user_id=None):
        if user_id is not None:
            return self.json_response_405()
        else:
            serializer = self.serializers(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return self.json_response_400()

    def put(self, request, user_id=None):
        if user_id is not None:
            queryset = get_object_or_404(self.model, id=user_id)
            data = request.data.copy()
            data["id"] = int(user_id)
            serializer = self.serializers(queryset, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return self.json_response_500()
        return self.json_response_405()

    def delete(self, request, user_id=None):
        if user_id is not None:
            queryset = get_object_or_404(self.model, id=user_id)
            if request.data.get("confirmation_key") == settings.DELETION_CONFIRMATION_KEY:
                queryset.delete()
                return self.json_response_204()
            else:
                return self.json_response_401()
        else:
            return self.json_response_405()
