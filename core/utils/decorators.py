from core.apps.common.models import Guild
from .mixins import ResponseMixin as Res


def permission_required(func):
    def wrapper(request, guild_id):
        if request.user.is_authenticated:
            try:
                guild = Guild.objects.get(id=guild_id)
            except Guild.DoesNotExist:
                return Res.html_response_404(request)
            if guild in request.user.admin.guilds.all():
                return func(request, guild_id)
            else:
                return Res.html_response_403(request)
        return Res.html_response_403(request)

    return wrapper
