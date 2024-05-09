from rest_framework import serializers

from .models import Feedback, FeedbackReply


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ("pk", "title", "message", "created_at", "updated_at")


class FeedbackReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackReply
        fields = ("pk", "message", "created_at", "updated_at")
