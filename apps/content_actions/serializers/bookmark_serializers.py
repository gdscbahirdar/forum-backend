from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.content_actions.constants import MODEL_MAPPING
from apps.content_actions.models.bookmark_models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bookmark model.

    This serializer is used to serialize and deserialize Bookmark objects.

    """

    class Meta:
        model = Bookmark
        fields = ("pk", "user", "content_type", "object_id", "created_at", "updated_at")
        read_only_fields = ("user", "content_type", "object_id")

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

        data["user"] = user
        data["content_type"] = content_type
        data["object_id"] = instance.id

        if (
            self.context["request"].method == "POST"
            and Bookmark.objects.filter(user=user, content_type=content_type, object_id=object_id).exists()
        ):
            raise ValidationError({"error": "You have already bookmarked the resource."})

        return data
