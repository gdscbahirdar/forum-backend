from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.content_actions.constants import MODEL_MAPPING
from apps.content_actions.models.comment_models import Comment
from apps.services.utils import check_toxicity


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    This serializer is used to serialize and deserialize Comment objects.

    """

    commented_by = serializers.SerializerMethodField()
    commenter_avatar = serializers.SerializerMethodField()

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
            "commenter_avatar",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "content_type", "object_id", "content_object", "vote_count", "commented_by")

    def get_commented_by(self, obj) -> str:
        return obj.user.username

    def get_commenter_avatar(self, obj) -> str:
        request = self.context.get("request")
        try:
            return request.build_absolute_uri(obj.user.avatar.url)
        except (AttributeError, ValueError):
            return ""

    def validate_text(self, value):
        if check_toxicity(value):
            raise serializers.ValidationError("The comment contains toxic content.")
        return value

    def validate(self, data):
        user = self.context["request"].user
        object_id = self.context["view"].kwargs["object_id"]
        model_name = self.context["view"].kwargs["model_name"]

        model = MODEL_MAPPING.get(model_name)
        if not model:
            raise ValidationError("Invalid model type")

        try:
            instance = model.objects.get(id=object_id)
            content_type = ContentType.objects.get_for_model(model)
        except model.DoesNotExist:
            raise ValidationError("Invalid object_id")

        data["content_type"] = content_type
        data["object_id"] = instance.id
        data["user"] = user

        return data
