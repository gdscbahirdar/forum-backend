from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import serializers

from apps.forum.models.qa_meta_models import Bookmark, Tag
from apps.forum.models.qa_models import Answer, Post, Question, Vote
from apps.forum.serializers.comment_serializers import CommentSerializer

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    user_vote = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at", "vote_count", "user_vote")

    def get_user_vote(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_anonymous:
                return None

            vote = Vote.objects.filter(user=user, content_type__model="post", object_id=obj.id).first()
            if vote:
                return vote.vote_type
            return None
        return None

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_anonymous:
                return False

            bookmark = Bookmark.objects.filter(user=user, content_type__model="post", object_id=obj.id).first()
            return bookmark is not None
        return False


class AnswerSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    answered_by = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ("id", "post", "answered_by", "is_accepted")

    def get_answered_by(self, obj) -> str:
        return obj.post.user.username

    def validate(self, data):
        question_slug = self.context.get("question_slug")
        if not question_slug:
            raise serializers.ValidationError("Question is required to create an answer.")

        question = Question.objects.filter(slug=question_slug).first()
        if not question:
            raise serializers.ValidationError("Question does not exist.")

        if question.is_closed:
            raise serializers.ValidationError("Answer can not be added to a closed question.")

        data["question"] = question
        return data

    def create(self, validated_data):
        post_data = validated_data.pop("post")
        post_user = self.context["request"].user
        post_data["user"] = post_user
        post = Post.objects.create(**post_data)
        answer = Answer.objects.create(post=post, **validated_data)
        return answer

    def update(self, instance, validated_data):
        post_data = validated_data.pop("post", None)
        instance = super().update(instance, validated_data)
        if post_data:
            post = instance.post
            for field, value in post_data.items():
                setattr(post, field, value)
            post.save()

        return instance


class BaseQuestionSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    tags = serializers.SlugRelatedField(slug_field="name", many=True, queryset=Tag.objects.all())
    asked_by = serializers.SerializerMethodField()
    accepted_answer = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(), required=False, allow_null=True
    )
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "slug",
            "post",
            "title",
            "tags",
            "is_answered",
            "is_closed",
            "view_count",
            "answer_count",
            "accepted_answer",
            "asked_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("view_count", "answer_count", "is_answered", "is_closed", "asked_by", "slug")

    def get_asked_by(self, obj) -> str:
        return obj.post.user.username

    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("The title must be at least 20 characters long.")
        return value

    def create(self, validated_data):
        post_data = validated_data.pop("post")
        post_user = self.context["request"].user
        post_data["user"] = post_user
        post = Post.objects.create(**post_data)
        slug = slugify(f"{validated_data['title']}-{int(datetime.now().timestamp())}")
        validated_data["slug"] = slug

        tags_data = validated_data.pop("tags", [])
        question = Question.objects.create(post=post, **validated_data)
        question.tags.set(tags_data)

        return question

    def update(self, instance, validated_data):
        post_data = validated_data.pop("post", None)
        tags_data = validated_data.pop("tags", [])

        if "title" in validated_data and validated_data["title"] != instance.title:
            slug = slugify(f"{validated_data['title']}-{int(datetime.now().timestamp())}")
            validated_data["slug"] = slug

        instance = super().update(instance, validated_data)
        instance.tags.set(tags_data)

        if post_data:
            post = instance.post
            for field, value in post_data.items():
                setattr(post, field, value)
            post.save()

        return instance


class QuestionSerializer(BaseQuestionSerializer):
    pass


class QuestionDetailSerializer(BaseQuestionSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta(BaseQuestionSerializer.Meta):
        fields = "__all__"


class BookmarkedPostSerializer(BaseQuestionSerializer):
    """
    Serializer class for bookmarked posts.

    This serializer is used to serialize bookmarked posts and their associated bookmarked answers.
    """

    bookmarked_answers = serializers.SerializerMethodField()

    class Meta(BaseQuestionSerializer.Meta):
        fields = (
            "id",
            "slug",
            "post",
            "title",
            "tags",
            "is_answered",
            "is_closed",
            "view_count",
            "answer_count",
            "asked_by",
            "created_at",
            "updated_at",
            "bookmarked_answers",
        )

    def get_bookmarked_answers(self, obj) -> list:
        """
        Retrieve the bookmarked answers for the given post.

        This method filters the bookmarked answers based on the current user and the associated bookmarks.
        It returns the serialized data of the bookmarked answers.
        """
        user = self.context["request"].user
        bookmarked_answers = Answer.objects.filter(
            post__bookmarks__user=user,
            question=obj,
            post__pk__in=Bookmark.objects.filter(user=user).values_list("object_id", flat=True),
        ).distinct()
        return AnswerSerializer(bookmarked_answers, many=True, context=self.context).data


class AcceptAnswerSerializer(serializers.Serializer):
    answer_id = serializers.UUIDField(help_text="Enter the ID of the answer to accept.")
