from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.badges.models.badge_models import UserBadge
from apps.badges.serializers.badge_serializer import UserBadgeSerializer
from apps.entities.models.faculty_models import Faculty

User = get_user_model()


class LeaderboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        timeframe = request.query_params.get("timeframe", "all")  # Default to 'all-time'
        today = timezone.localdate()
        start_of_week = today - timedelta(days=today.weekday())  # Monday

        # In the future when we have multiple faculties, this should be dynamic
        faculty = Faculty.objects.filter(name="Faculty of Computing").first()
        users = User.objects.filter(
            Q(student__faculty=faculty) | Q(teacher__faculty=faculty) | Q(faculty_admin__faculty=faculty)
        )

        if timeframe == "daily":
            date_filter = today
        elif timeframe == "weekly":
            date_filter = start_of_week
        else:
            date_filter = None  # For all-time, no date filtering

        if date_filter:
            users = (
                users.filter(daily_reputations__reputation__isnull=False)
                .annotate(
                    total_reputation=Sum(
                        "daily_reputations__reputation", filter=Q(daily_reputations__date__gte=date_filter)
                    )
                )
                .order_by("-total_reputation")
            )
        else:
            users = users.order_by("-reputation")

        data = [
            {
                "rank": rank + 1,
                "fullname": user.get_fullname,
                "avatar": user.avatar.url if user.avatar else None,
                "reputation": user.total_reputation if date_filter else user.reputation,
            }
            for rank, user in enumerate(users[:10])  # top 10 users
        ]

        return Response(data)


class UserBadgesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        user_badges = UserBadge.objects.filter(user=user).select_related("badge")
        serializer = UserBadgeSerializer(user_badges, many=True)
        return Response(serializer.data)
