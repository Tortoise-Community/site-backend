from django.contrib import admin

from .models import User, Guild, Member

admin.site.register([User, Guild, Member])
