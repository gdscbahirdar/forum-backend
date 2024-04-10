from datetime import datetime
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import serializers

from apps.forum.models.comment_models import Comment
from apps.forum.models.qa_models import Post, Question, Answer
from apps.forum.models.tag_models import Tag

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("user", "created_at", "updated_at")


class AnswerSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "post", "question", "user", "comments"]

    def get_user(self, obj):
        return obj.post.user.username

    def validate(self, data):
        question = data.get("question")

        if not question:
            raise serializers.ValidationError("Question is required to create an answer.")

        question = Question.objects.filter(id=question).first()

        if not question:
            raise serializers.ValidationError("Question does not exist.")

        if question.is_closed:
            raise serializers.ValidationError("Answer can not be added to a closed question.")

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
        if post_data:
            Post.objects.filter(id=instance.post.id).update(**post_data)
        return super().update(instance, validated_data)


class BaseQuestionSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    user = serializers.SerializerMethodField()
    accepted_answer = serializers.PrimaryKeyRelatedField(
        queryset=Answer.objects.all(), required=False, allow_null=True
    )
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "post",
            "title",
            "tags",
            "is_answered",
            "is_closed",
            "view_count",
            "answer_count",
            "accepted_answer",
            "user",
            "slug",
        ]

    def get_user(self, obj):
        return obj.post.user.username

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
        if post_data:
            Post.objects.filter(id=instance.post.id).update(**post_data)

        if "title" in validated_data:
            slug = slugify(f"{validated_data['title']}-{int(datetime.now().timestamp())}")
            validated_data["slug"] = slug

        tags_data = validated_data.pop("tags", [])
        instance.tags.set(tags_data)

        return super().update(instance, validated_data)


class QuestionSerializer(BaseQuestionSerializer):
    pass


class QuestionDetailSerializer(BaseQuestionSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta(BaseQuestionSerializer.Meta):
        fields = "__all__"
