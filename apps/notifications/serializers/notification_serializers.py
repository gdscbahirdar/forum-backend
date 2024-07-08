from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from apps.forum.models.qa_models import Answer
from apps.forum.models.qa_models import Question
from apps.notifications.models.notification_models import Notification
from apps.notifications.models.notification_models import Subscription
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

    target_type = serializers.SerializerMethodField()
    target_slug = serializers.SerializerMethodField()
    subscription_id = serializers.SerializerMethodField()

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
            "target_type",
            "target_slug",
            "subscription_id",
        )

    def get_target_slug(self, obj) -> str:
        """
        Returns the slug of the target object.
        """
        target = obj.target
        if isinstance(target, Question):
            return target.slug
        elif isinstance(target, Answer):
            return target.question.slug
        return ""

    def get_target_type(self, obj) -> str:
        """
        Returns the type of the target object.
        """
        target = obj.target
        if isinstance(target, Question):
            return "question"
        elif isinstance(target, Answer):
            return "answer"
        elif isinstance(target, Resource):
            return "resource"
        return ""

    def get_subscription_id(self, obj) -> str:
        """
        Returns the subscription ID for the notification.
        """
        user = self.context["request"].user
        target_content_type = ContentType.objects.get_for_model(obj.target)
        subscription = Subscription.objects.filter(
            user=user, target_content_type=target_content_type, target_object_id=obj.target_object_id
        ).first()
        return subscription.id if subscription else ""
