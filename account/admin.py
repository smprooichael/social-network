from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Relations


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class ExtendingUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, ExtendingUserAdmin)
admin.site.register(Relations)