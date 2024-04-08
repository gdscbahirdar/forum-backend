from dj_rest_auth.views import PasswordChangeView


class ChangePasswordView(PasswordChangeView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = request.user
        if getattr(user, "is_first_time_login", False):
            user.is_first_time_login = False
            user.save(update_fields=["is_first_time_login"])
        return response
