from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    """
    Custom permission class that allows access only to the owner of an object or superusers.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.user == request.user
