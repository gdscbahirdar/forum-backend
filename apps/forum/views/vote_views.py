from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.forum.models.qa_meta_models import Vote
from apps.forum.serializers.vote_serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling vote operations.

    This viewset allows users to perform CRUD operations (Create, Retrieve, Update, Delete) on Vote objects.
    Only authenticated users are allowed to access this viewset.
    """

    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer
