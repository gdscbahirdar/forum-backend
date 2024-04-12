from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.forum.models.comment_models import Comment
from apps.forum.models.vote_models import Vote


class Post(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField(_("Post Body"))
    vote_count = models.IntegerField(default=0)
    comments = GenericRelation(Comment)
    votes = GenericRelation(Vote, related_query_name="post")

    def __str__(self):
        return f"Post by {self.user}"


class Question(BaseModel):
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
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.title


class Answer(BaseModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title}"
