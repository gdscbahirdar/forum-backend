from django.contrib import admin

from apps.rbac.models.role_models import Module
from apps.rbac.models.role_models import Permission
from apps.rbac.models.role_models import Role
from apps.rbac.models.role_models import UserRole


class PermissionInline(admin.TabularInline):
    model = Permission
    extra = 1


class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1


class ModuleAdmin(admin.ModelAdmin):
    inlines = [PermissionInline]
    list_display = ("name",)


class RoleAdmin(admin.ModelAdmin):
    inlines = [UserRoleInline]
    list_display = ("name",)
    filter_horizontal = ("permissions",)


admin.site.register(Module, ModuleAdmin)
admin.site.register(Role, RoleAdmin)
