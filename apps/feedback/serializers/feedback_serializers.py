from rest_framework import serializers

from apps.feedback.models.feedback_models import Feedback
from apps.feedback.models.feedback_models import FeedbackReply


class FeedbackSerializer(serializers.ModelSerializer):
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ("pk", "author_avatar", "title", "message", "created_at", "updated_at")

    def get_author_avatar(self, obj) -> str:
        request = self.context.get("request")
        try:
            return request.build_absolute_uri(obj.user.avatar.url)
        except (AttributeError, ValueError):
            return ""


class FeedbackReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackReply
        fields = ("pk", "message", "created_at", "updated_at")
