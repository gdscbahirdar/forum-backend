from rest_framework import serializers
from apps.resources.models.resource_models import ResourceCategory, Resource, ResourceFile
from apps.forum.models import Tag


class ResourceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceFile
        fields = ["id", "file"]

    def validate(self, data):
        if data["file"].size > 100 * 1024 * 1024:
            raise serializers.ValidationError("File size is greater than 100MB")


class ResourceSerializer(serializers.ModelSerializer):
    files = ResourceFileSerializer(many=True, required=False)
    uploader = serializers.ReadOnlyField(source="uploader.username")
    tags = serializers.SlugRelatedField(slug_field="name", queryset=Tag.objects.all(), many=True)
    categories = serializers.SlugRelatedField(slug_field="name", queryset=ResourceCategory.objects.all(), many=True)

    class Meta:
        model = Resource
        fields = ["id", "title", "description", "created_at", "updated_at", "uploader", "categories", "tags", "files"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        categories_data = validated_data.pop("categories")
        files_data = validated_data.pop("files", [])
        resource = Resource.objects.create(**validated_data)
        for tag_data in tags_data:
            resource.tags.add(tag_data)
        for category_data in categories_data:
            resource.categories.add(category_data)
        for file_data in files_data:
            ResourceFile.objects.create(resource=resource, **file_data)
        return resource

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", None)
        categories_data = validated_data.pop("categories", None)
        files_data = validated_data.pop("files", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)

        if categories_data is not None:
            instance.categories.set(categories_data)

        if files_data is not None:
            instance.files.all().delete()
            for file_data in files_data:
                ResourceFile.objects.create(resource=instance, **file_data)

        return instance
