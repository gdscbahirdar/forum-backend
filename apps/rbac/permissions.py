from rest_framework.permissions import BasePermission

from apps.rbac.models.role_models import UserRole


class IsUserSuperAdmin(BasePermission):
    """
    Custom permission class to check if the user is a Super Admin.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has the permission to access the view.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        try:
            user_role = UserRole.objects.get(user=request.user)
            return user_role.role.name == "Super Admin"
        except UserRole.DoesNotExist:
            return False


class IsUserFacultyAdmin(BasePermission):
    """
    Custom permission class to check if the user is a Faculty Admin.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        try:
            user_role = UserRole.objects.get(user=request.user)
            return user_role.role.name == "Faculty Admin"
        except UserRole.DoesNotExist:
            return False


class IsUserSuperAdminOrFacultyAdmin(BasePermission):
    """
    Custom permission class to check if the user is a Super Admin or Faculty Admin.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        try:
            user_role = UserRole.objects.get(user=request.user)
            return user_role.role.name in ["Super Admin", "Faculty Admin"]
        except UserRole.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.
            obj (object): The object being accessed.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        try:
            user_role = UserRole.objects.get(user=request.user)
            return user_role.role.name == "Super Admin" or obj.faculty == request.user.faculty_admin.faculty
        except UserRole.DoesNotExist:
            return False
