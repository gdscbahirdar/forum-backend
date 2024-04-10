from django.contrib.auth import get_user_model
from django_filters import rest_framework as django_filters
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.entities.serializers.entity_serializers import EntitySerializer
from apps.rbac.permissions import IsUserSuperAdmin, IsUserSuperAdminOrFacultyAdmin

User = get_user_model()


class EntityViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing entities.

    This viewset provides CRUD operations for entities and applies permissions based on the entity type.

    Attributes:
        permission_classes (tuple): A tuple of permission classes to apply for the viewset.
        serializer_class (Serializer): The serializer class to use for serializing and deserializing entities.

    Methods:
        get_permissions(): Returns the permission classes based on the action and entity type.
        get_queryset(): Returns the queryset of entities based on the entity type and user role.
        get_serializer_context(): Overrides the default method to add the 'entity_type' to the serializer context.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = EntitySerializer
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = (
        "student__faculty",
        "student__department",
        "student__department__name",
        "student__year_in_school",
        "teacher__faculty",
        "teacher__departments",
    )
    search_fields = ("username", "first_name", "middle_name", "last_name")
    ordering_fields = ("username",)
    ordering = ("username",)

    def get_permissions(self):
        """
        Returns the permission classes based on the action and entity type.

        If the action is 'create' and the entity type is 'faculty_admin', adds 'IsUserSuperAdmin' permission class.
        Otherwise, adds 'IsUserSuperAdminOrFacultyAdmin' permission class.

        Returns:
            tuple: A tuple of permission classes.
        """
        if self.action == "create":
            if self.kwargs.get("entity_type") == "faculty_admin":
                self.permission_classes += (IsUserSuperAdmin,)
            else:
                self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)
        else:
            self.permission_classes += (IsUserSuperAdminOrFacultyAdmin,)

        return super().get_permissions()

    def get_queryset(self):
        """
        Returns the queryset of entities based on the entity type and user role.

        Filters the queryset based on the entity type.
        If the user has a 'user_role' attribute and it's not 'Super Admin', filters by faculty.

        Returns:
            QuerySet: The filtered queryset of entities.
        """
        entity_type = self.kwargs.get("entity_type")
        filter = {f"{entity_type}__isnull": False}
        queryset = User.objects.filter(**filter)

        if hasattr(self.request.user, "user_role") and self.request.user.user_role.role.name != "Super Admin":
            faculty = self.request.user.faculty_admin.faculty
            queryset = queryset.filter(faculty=faculty)

        return queryset

    def get_serializer_context(self):
        """
        Overrides the default method to add the 'entity_type' to the serializer context.

        Returns:
            dict: The serializer context with the 'entity_type' added.
        """
        context = super().get_serializer_context()
        entity_type = self.kwargs.get("entity_type")
        context.update({"entity_type": entity_type})
        return context
