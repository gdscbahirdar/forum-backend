from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import serializers

from apps.forum.models.qa_models import Answer, Question
from apps.notifications.models.notification_models import Notification, Subscription
from apps.resources.models.resource_models import Resource


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Subscription model.
    """

    target_content_type = serializers.SlugRelatedField(
        slug_field="model", queryset=ContentType.objects.filter(model__in=("question", "answer", "resource"))
    )
    target_object_id = serializers.UUIDField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ("id", "user", "target_content_type", "target_object_id", "target")
        read_only_fields = ("user",)

    def get_target(self, obj) -> str:
        return str(obj.target)

    def validate(self, data):
        target_content_type = data["target_content_type"]
        target_object_id = data["target_object_id"]

        model_class = target_content_type.model_class()
        try:
            model_class.objects.get(pk=target_object_id)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("The specified target object does not exist.")

        if Subscription.objects.filter(
            user=self.context["request"].user,
            target_content_type=target_content_type,
            target_object_id=target_object_id,
        ).exists():
            raise serializers.ValidationError("You are already subscribed to this content.")

        return data


class NotificationReadOnlySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Notification model in read-only mode.
    """

    target_url = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id",
            "level",
            "title",
            "message",
            "is_read",
            "created_at",
            "updated_at",
            "target_object_id",
            "target_url",
        )

    def get_target_url(self, obj) -> str:
        """
        Generates the URL for the target object based on its type.
        """
        target = obj.target
        if isinstance(target, Question):
            return reverse("forum:question-detail", kwargs={"slug": target.slug})
        elif isinstance(target, Answer):
            return reverse("forum:answer-detail", kwargs={"question_slug": target.question.slug, "pk": target.pk})
        elif isinstance(target, Resource):
            return reverse("resources:resource-detail", kwargs={"pk": target.pk})
        return ""
