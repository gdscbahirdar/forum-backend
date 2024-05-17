from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetView, UserDetailsView
from django.urls import path

from apps.users.views.auth_views import ChangePasswordView
from apps.users.views.user_views import GetUserBookmarkList, UserListView, UserProfileView

rest_auth_urls = [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
]


rest_password_urls = [
    path("password/change/", ChangePasswordView.as_view(), name="rest_password_change"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]

meta_urls = [
    path("user/bookmarks/", GetUserBookmarkList.as_view(), name="user_bookmarks"),
    path("", UserListView.as_view(), name="user_list"),
    path("<str:username>/", UserProfileView.as_view(), name="user_profile"),
]

urlpatterns = rest_auth_urls + rest_password_urls + meta_urls
