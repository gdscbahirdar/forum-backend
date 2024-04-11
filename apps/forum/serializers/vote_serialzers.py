from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType

from apps.forum.models.vote_models import Vote
from apps.forum.models.qa_models import Post
from apps.forum.models.comment_models import Comment


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = "__all__"
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

        if existing_vote and existing_vote.vote_type == vote_type:
            raise ValidationError(f"You cannot {vote_type} more than once.")

        return data

    def update_vote_count(self, vote_type, instance, change):
        post = instance.content_object

        if vote_type == Vote.UPVOTE:
            post.vote_count += change
        elif vote_type == Vote.DOWNVOTE:
            post.vote_count -= change
        post.save()

    def create(self, validated_data):
        vote_type = validated_data["vote_type"]

        existing_vote = validated_data.pop("existing_vote", None)
        if existing_vote:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            self.update_vote_count(vote_type, existing_vote, 2)
            return existing_vote

        instance = super().create(validated_data)
        self.update_vote_count(vote_type, instance, 1)
        return instance
