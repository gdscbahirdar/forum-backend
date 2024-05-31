from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.content_actions.constants import MODEL_MAPPING
from apps.content_actions.models.vote_models import Vote


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("pk", "user", "content_type", "object_id", "vote_type", "created_at", "updated_at")
        read_only_fields = ("user", "content_type")

    def validate(self, data):
        user = self.context["request"].user
        object_id = data["object_id"]
        vote_type = data["vote_type"]
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

        if vote_type not in (Vote.UPVOTE, Vote.DOWNVOTE):
            raise ValidationError("Invalid vote_type")

        existing_vote = Vote.objects.filter(user=user, content_type=content_type, object_id=object_id).first()
        data["existing_vote"] = existing_vote

        return data

    def update_vote_count(self, vote_type, instance, change):
        model_instance = instance.content_object
        user = model_instance.user

        if vote_type == Vote.UPVOTE:
            model_instance.vote_count += change
            if instance.vote_type == Vote.DOWNVOTE:
                user.add_reputation(12)
            else:
                user.add_reputation(10)
        elif vote_type == Vote.DOWNVOTE:
            model_instance.vote_count -= change
            if instance.vote_type == Vote.UPVOTE:
                user.subtract_reputation(12)
            else:
                user.subtract_reputation(2)

        model_instance.save()
        model_instance.update_score()
        model_instance.evaluate_score_badges()

    def create(self, validated_data):
        vote_type = validated_data["vote_type"]
        existing_vote = validated_data.pop("existing_vote", None)

        # TODO The vote deletion logic should be refactored to a separate endpoint.
        if existing_vote and existing_vote.vote_type == vote_type:
            model_instance = existing_vote.content_object
            user = model_instance.user
            if vote_type == Vote.UPVOTE:
                model_instance.vote_count += -1
                user.subtract_reputation(10)

            if vote_type == Vote.DOWNVOTE:
                model_instance.vote_count += 1
                user.add_reputation(2)

            model_instance.save()
            existing_vote.delete()
            return existing_vote

        if existing_vote:
            self.update_vote_count(vote_type, existing_vote, 2)
            existing_vote.vote_type = vote_type
            existing_vote.save()
            return existing_vote

        instance = super().create(validated_data)
        self.update_vote_count(vote_type, instance, 1)
        return instance
