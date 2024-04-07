from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Module(BaseModel):
    """
    Represents a module in the RBAC system.

    Attributes:
        name (str): The name of the module.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Permission(BaseModel):
    """
    Represents a permission in the system.

    Attributes:
        name (str): The name of the permission.
        module (Module): The module to which the permission belongs.
    """

    name = models.CharField(max_length=50)
    module = models.ForeignKey(Module, related_name="permissions", on_delete=models.CASCADE)

    def __str__(self):
        return f"Module: {self.module} - Permission: {self.name}"


class Role(BaseModel):
    """
    Represents a role in the system.

    Attributes:
        name (str): The name of the role.
        permissions (ManyToManyField): The permissions associated with the role.
    """

    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return f"Role: {self.name}"


class UserRole(BaseModel):
    """
    Represents the relationship between a user and a role.

    Attributes:
        user (User): The user associated with the role.
        role (Role): The role associated with the user.
        created_at (datetime): The timestamp when the user-role relationship was created.
        updated_at (datetime): The timestamp when the user-role relationship was last updated.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="user_role", on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"User: {self.user} - {self.role}"
