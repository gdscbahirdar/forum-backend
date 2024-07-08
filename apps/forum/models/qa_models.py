from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.content_actions.models.bookmark_models import Bookmark
from apps.content_actions.models.comment_models import Comment
from apps.content_actions.models.view_models import ViewTracker
from apps.content_actions.models.vote_models import Vote


class Post(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField(_("Post Body"))
    vote_count = models.IntegerField(default=0)
    comments = GenericRelation(Comment)
    votes = GenericRelation(Vote, related_query_name="post")
    bookmarks = GenericRelation(Bookmark, related_query_name="post")
    score = models.IntegerField(default=0, help_text="The score of the post. upvotes - downvotes.")

    def __str__(self):
        return f"Post by {self.user}"

    def update_score(self):
        upvotes = self.votes.filter(vote_type=Vote.UPVOTE).count()
        downvotes = self.votes.filter(vote_type=Vote.DOWNVOTE).count()
        self.score = upvotes - downvotes
        self.save(update_fields=["score"])

    def evaluate_score_badges(self):
        question = getattr(self, "question", None)
        answer = getattr(self, "answer", None)
        if question:
            self.check_question_score_badges()
        if answer:
            self.check_answer_score_badges(answer)

    def check_question_score_badges(self):
        if self.score >= 100:
            self.user.assign_badge("Great Question")
        elif self.score >= 25:
            self.user.assign_badge("Good Question")
        elif self.score >= 10:
            self.user.assign_badge("Nice Question")

    def check_answer_score_badges(self, answer):
        if self.score >= 100:
            self.user.assign_badge("Great Answer")
        elif self.score >= 25:
            self.user.assign_badge("Good Answer")
        elif self.score >= 10:
            self.user.assign_badge("Nice Answer")
        elif self.score >= 3 and self.user == answer.question.post.user:
            self.user.assign_badge("Self-Learner")
        elif self.score >= 1:
            self.user.assign_badge("Teacher")

    def evaluate_bookmark_badges(self):
        question = getattr(self, "question", None)
        answer = getattr(self, "answer", None)
        if question:
            self.check_question_bookmark_badges()
        if answer:
            self.check_answer_bookmark_badges()

    def check_question_bookmark_badges(self):
        if self.bookmarks.count() >= 100:
            self.user.assign_badge("Stellar Question")
        elif self.bookmarks.count() >= 25:
            self.user.assign_badge("Favorite Question")

    def check_answer_bookmark_badges(self):
        if self.bookmarks.count() >= 100:
            self.user.assign_badge("Stellar Answer")
        elif self.bookmarks.count() >= 25:
            self.user.assign_badge("Favorite Answer")


class Question(BaseModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="question")
    title = models.CharField(max_length=150, db_index=True)
    tags = models.ManyToManyField("Tag", related_name="questions")
    is_answered = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    answer_count = models.PositiveIntegerField(default=0)
    accepted_answer = models.ForeignKey(
        "Answer", on_delete=models.SET_NULL, null=True, blank=True, related_name="accepted_by_question"
    )
    slug = models.SlugField(max_length=255, unique=True)
    views = GenericRelation(ViewTracker, related_query_name="question")

    def __str__(self):
        return self.title

    def check_question_view_badges(self):
        if self.view_count >= 10_000:
            self.post.user.assign_badge("Famous Question")
        elif self.view_count >= 2500:
            self.post.user.assign_badge("Notable Question")
        elif self.view_count >= 1000:
            self.post.user.assign_badge("Popular Question")


class Answer(BaseModel):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="answer")
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title}"
