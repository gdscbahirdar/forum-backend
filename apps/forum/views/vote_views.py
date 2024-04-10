from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.forum.models.vote_models import Vote
from apps.forum.serializers.vote_serialzers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = VoteSerializer
