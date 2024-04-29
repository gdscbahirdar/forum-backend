from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.forum.models.qa_meta_models import Bookmark
from apps.forum.models.qa_models import Post


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

        if Bookmark.objects.filter(user=user, content_type=content_type, object_id=object_id).exists():
            raise ValidationError({"error": "You have already bookmarked the resource."})

        return data
