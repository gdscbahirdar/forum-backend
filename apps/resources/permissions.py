from rest_framework.permissions import BasePermission


class IsOwnerOrSuperUser(BasePermission):
    """
    Custom permission class that allows access only to the owner of an object or superusers.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.uploader == request.user


class IsOwner(BasePermission):
    """
    Custom permission class that allows access only to the owner of an object.
    """

    def has_object_permission(self, request, view, obj):
        return obj.uploader == request.user


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
