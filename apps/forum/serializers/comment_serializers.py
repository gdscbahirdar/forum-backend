from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.forum.models.qa_meta_models import Comment
from apps.forum.models.qa_models import Post
from apps.services.utils import check_toxicity


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    This serializer is used to serialize and deserialize Comment objects.

    """

    commented_by = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "pk",
            "user",
            "content_type",
            "object_id",
            "text",
            "vote_count",
            "commented_by",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "content_type", "object_id", "content_object", "vote_count", "commented_by")

    def get_commented_by(self, obj) -> str:
        return obj.user.username

    def validate_text(self, value):
        if check_toxicity(value):
            raise serializers.ValidationError("The comment contains toxic content.")
        return value

    def validate(self, data):
        object_id = self.context.get("object_id")

        try:
            Post.objects.get(pk=object_id)
        except Post.DoesNotExist:
            raise ValidationError({"error": "Resource not found."})

        content_type = ContentType.objects.get_for_model(Post)
        user = self.context["request"].user
        data["user"] = user
        data["content_type"] = content_type
        data["object_id"] = object_id

        return data
