from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.forum.models.qa_meta_models import Comment, Vote
from apps.forum.models.qa_models import Post


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ("pk", "user", "content_type", "object_id", "vote_type", "created_at", "updated_at")
        read_only_fields = ("user", "content_type")

    def validate(self, data):
        user = self.context["request"].user
        object_id = data["object_id"]
        vote_type = data["vote_type"]

        try:
            instance = Post.objects.get(id=object_id)
            content_type = ContentType.objects.get_for_model(Post)
        except Post.DoesNotExist:
            try:
                instance = Comment.objects.get(id=object_id)
                content_type = ContentType.objects.get_for_model(Comment)
            except Comment.DoesNotExist:
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
        post: Post = instance.content_object
        user = post.user

        if vote_type == Vote.UPVOTE:
            post.vote_count += change
            if instance.vote_type == Vote.DOWNVOTE:
                user.add_reputation(12)
            else:
                user.add_reputation(10)
        elif vote_type == Vote.DOWNVOTE:
            post.vote_count -= change
            if instance.vote_type == Vote.UPVOTE:
                user.subtract_reputation(12)
            else:
                user.subtract_reputation(2)

        post.save()
        post.update_score()
        post.evaluate_score_badges()

    def create(self, validated_data):
        vote_type = validated_data["vote_type"]
        existing_vote = validated_data.pop("existing_vote", None)

        # TODO The vote deletion logic should be refactored to a separate endpoint.
        if existing_vote and existing_vote.vote_type == vote_type:
            self.update_vote_count(vote_type, existing_vote, -1)
            existing_vote.delete()
            return existing_vote

        if existing_vote:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            self.update_vote_count(vote_type, existing_vote, 2)
            return existing_vote

        instance = super().create(validated_data)
        self.update_vote_count(vote_type, instance, 1)
        return instance
