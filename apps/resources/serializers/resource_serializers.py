from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.models.vote_models import Vote
from apps.content_actions.serializers.comment_serializers import CommentSerializer
from apps.forum.models import Tag
from apps.notifications.models.notification_models import Subscription
from apps.resources.constants import ResourceConstants
from apps.resources.models.resource_models import Resource
from apps.resources.models.resource_models import ResourceCategory
from apps.resources.models.resource_models import ResourceFile


class ResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceFile
        fields = ("id", "file", "file_name", "file_type", "file_size")

    def validate(self, data):
        if data["file"].size > 100 * 1024 * 1024:
            raise serializers.ValidationError("File size is greater than 100MB")

    def create(self, validated_data):
        return ResourceFile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.file = validated_data.get("file", instance.file)
        instance.save()
        return instance


class ResourceSerializer(serializers.ModelSerializer):
    files = ResourceFileSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source="user.username")
    tags = serializers.SlugRelatedField(slug_field="name", queryset=Tag.objects.all(), many=True)
    categories = serializers.SlugRelatedField(slug_field="name", queryset=ResourceCategory.objects.all(), many=True)
    comments = CommentSerializer(many=True, read_only=True)
    user_vote = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    subscription_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Resource
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "user",
            "categories",
            "tags",
            "files",
            "comments",
            "view_count",
            "vote_count",
            "user_vote",
            "is_bookmarked",
            "subscription_id",
        )
        read_only_fields = (
            "view_count",
            "vote_count",
        )

    def get_user_vote(self, obj) -> str:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            vote = Vote.objects.filter(user=user, content_type__model="resource", object_id=obj.id).first()
            return vote.vote_type if vote else ""
        return ""

    def get_is_bookmarked(self, obj) -> bool:
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            bookmark = Bookmark.objects.filter(user=user, content_type__model="resource", object_id=obj.id).first()
            return bookmark is not None
        return False

    def get_subscription_id(self, obj) -> str:
        user = self.context["request"].user
        content_type = ContentType.objects.get(model="resource")
        subscription = Subscription.objects.filter(
            user=user, target_content_type=content_type, target_object_id=obj.id
        ).first()
        return subscription.id if subscription else ""

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        categories_data = validated_data.pop("categories")
        files_data = self.context["request"].FILES.getlist("files")
        files_to_delete = validated_data.pop("filesToDelete", [])

        resource = Resource.objects.create(**validated_data)

        resource.tags.set(tags_data)
        resource.categories.set(categories_data)

        for file_data in files_data:
            file_instance = ResourceFile.objects.create(resource=resource, file=file_data)
            file_instance.file_type = ResourceConstants.FILE_TYPE_MAPPING[file_data.content_type]
            file_instance.file_size = file_data.size
            file_instance.save()

        for file_id in files_to_delete:
            ResourceFile.objects.get(id=file_id).delete()

        return resource

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        categories_data = validated_data.pop("categories", None)
        files_data = self.context["request"].FILES.getlist("files")
        files_to_delete = self.context["request"].data.getlist("filesToDelete")

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        if categories_data is not None:
            instance.categories.set(categories_data)

        if files_data is not None:
            for file_data in files_data:
                file_instance = ResourceFile.objects.create(resource=instance, file=file_data)
                file_instance.file_type = ResourceConstants.FILE_TYPE_MAPPING[file_data.content_type]
                file_instance.file_size = file_data.size
                file_instance.save()

        for file_id in files_to_delete:
            ResourceFile.objects.get(id=file_id).delete()

        return instance


class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = ("id", "name", "description")


class BookmarkedResourceSerializer(ResourceSerializer):
    """
    Serializer class for bookmarked resources.
    """

    class Meta(ResourceSerializer.Meta):
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "user",
            "categories",
            "tags",
            "files",
            "comments",
            "view_count",
            "vote_count",
        )
