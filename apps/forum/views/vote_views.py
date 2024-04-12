from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.forum.models.vote_models import Vote
from apps.forum.serializers.vote_serialzers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling vote operations.

    This viewset allows users to perform CRUD operations (Create, Retrieve, Update, Delete) on Vote objects.
    Only authenticated users are allowed to access this viewset.

    Attributes:
        queryset (QuerySet): The queryset of all Vote objects.
        permission_classes (tuple): The permission classes required to access this viewset.
        serializer_class (Serializer): The serializer class used for serializing and deserializing Vote objects.
    """

    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer
