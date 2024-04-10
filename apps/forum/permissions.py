from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission class that allows only the owner of an object to modify it,
    while allowing read-only access to other users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the requested action on the object.

        Args:
            request (HttpRequest): The request being made.
            view (View): The view handling the request.
            obj (object): The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if request.user.is_superuser:
            return True
        # TODO make sure to check if the user is a faculty admin
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return obj.user == request.user
