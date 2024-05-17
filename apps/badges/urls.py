from django.urls import path

from apps.badges.views.badge_views import LeaderboardView, UserBadgesView

app_name = "badges"

urlpatterns = [
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("user/<str:username>/badges/", UserBadgesView.as_view(), name="user-badges"),
]
