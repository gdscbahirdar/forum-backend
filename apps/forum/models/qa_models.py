from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from apps.common.models import BaseModel
from apps.forum.models.comment_models import Comment


class Post(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField(_("Post Body"))
    vote_count = models.IntegerField(default=0)


class Question(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="question")
    title = models.CharField(max_length=255, db_index=True)
    tags = models.ManyToManyField("Tag", related_name="questions")
    is_answered = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    accepted_answer = models.ForeignKey(
        "Answer", on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_by_question"
    )
    comments = GenericRelation(Comment)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["post__created_at"]

    def __str__(self):
        return self.title


class Answer(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"Answer to {self.question.title}"
