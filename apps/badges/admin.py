from django.contrib import admin

from apps.badges.models.badge_models import DailyUserReputation

from .models import Badge, UserBadge


class UserBadgeInline(admin.TabularInline):
    model = UserBadge
    extra = 1


class BadgeAdmin(admin.ModelAdmin):
    inlines = (UserBadgeInline,)


admin.site.register(Badge, BadgeAdmin)
admin.site.register(DailyUserReputation)
